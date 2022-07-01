#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path, mkdir
from enum import Enum
import json, wget

# if true print informations on stdout
OUT = True

# folders
DATAS_DIR = "datas/"
RESULTS_DIR_TEMPLATE = "results_rrc{}_{:04n}{:02n}/"
SESSION_DIR_TEMPLATE = "datas_rrc{}_{:04n}{:02n}/"
RESULTS_DIR = ""
SESSION_DIR = ""

# input datas
FRENCH_PREFIXES_JSON = DATAS_DIR + "french_prefixes.json"
FRENCH_AS_JSON = DATAS_DIR + "AS_FR.json"
ALL_FR_SUBNETS_JSON = DATAS_DIR + "all_fr_subnets.json"

# output files
MOAS_OUT_JSON = ""
COUNTRY_OUT_JSON = ""
HISTORY_JSON = ""
MORE_SPEC_JSON = ""

# collectors
collectors = [6,14,26]

# year and month
ym=[2022,6]

# watcher/history start_day end_day
sd = 28
ed = 30

# number of update to watch
count = 5

def setup():
    """
    Check for existing input and output directories
    Set output filenames
    """
    if not path.exists("bgpdump"):
        Affich.error(0, "bgpdump not found, please buid it")
        exit(0)
    if not path.isdir(DATAS_DIR): mkdir("datas", 0o755)
    y,m=ym
    global RESULTS_DIR, SESSION_DIR, HISTORY_JSON, MOAS_OUT_JSON, COUNTRY_OUT_JSON, MORE_SPEC_JSON
    RESULTS_DIR = RESULTS_DIR_TEMPLATE.format("-".join(["{:02n}".format(_) for _ in collectors]), y,m)
    SESSION_DIR = SESSION_DIR_TEMPLATE.format("-".join(["{:02n}".format(_) for _ in collectors]), y,m)
    if not path.isdir(RESULTS_DIR): mkdir(RESULTS_DIR, 0o755)
    if not path.isdir(SESSION_DIR): mkdir(SESSION_DIR, 0o755)
    MOAS_OUT_JSON = RESULTS_DIR + "moas-rrc{}-{:04n}{:02n}.json".format("-".join(["{:02n}".format(_) for _ in collectors]), y,m)
    COUNTRY_OUT_JSON = RESULTS_DIR + "country-rrc{}-{:04n}{:02n}.json".format("-".join(["{:02n}".format(_) for _ in collectors]), y,m)
    HISTORY_JSON = RESULTS_DIR + "history-rrc{}-{:04n}{:02n}.json".format("-".join(["{:02n}".format(_) for _ in collectors]), y,m)
    MORE_SPEC_JSON = RESULTS_DIR + "more-spec-rrc{}-{:04n}{:02n}.json".format("-".join(["{:02n}".format(_) for _ in collectors]), y,m)


def load_json_file(source:str)->dict:
    """
    Load a json file into a dict
    """
    with open(source, "r") as jf:
        return json.load(jf)

def save_json_file(d:dict, name:str):
    """
    Save dict to json file
    """
    with open(name,"w") as jf:
        json.dump(d, jf, indent=4)

def menu():
    """
    Print menu informations
    """
    y,m = ym
    msg = """BGP watcher
    Collectors : {}
    History : {:02n} to {:02n} of {:02n}-{:04n}
    """.format("/".join(map(str,collectors)), sd, ed, m, y)
    print(msg)

def download(url:str, out:str):
    """
    Custom download using wget
    """
    try:
        wget.download(url, out, bar=None)
    except:
        Affich.error(0, "Unable to download " + url)
        exit(-1)

class Affich(Enum):
    """
    Code inspired by https://github.com/MrrRaph
    """
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    @staticmethod
    def success(indent:int, msg:str):
        if OUT: print("\t" * indent + f"[{Affich.GREEN.value}+{Affich.RESET.value}] {msg}")

    @staticmethod
    def info(indent:int, msg:str):
        if OUT: print("\t" * indent + f"[{Affich.BLUE.value}*{Affich.RESET.value}] {msg}")

    @staticmethod
    def error(indent:int, msg:str):
        if OUT: print("\t" * indent + f"[{Affich.RED.value}!{Affich.RESET.value}] {msg}")

    @staticmethod
    def event(indent:int, p:str, a:list, t:str):
        if OUT: print("\t" * indent + f"[{Affich.CYAN.value}>{Affich.RESET.value}] Prefix {p}\t announced by {'/'.join(map(str, a))}\t Tag {t}")
