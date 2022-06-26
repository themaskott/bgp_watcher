#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# mostly adapted from https://github.com/formtapez/ripe

# import from python
import gzip, time, logging, re, os.path, math, wget, json
from multiprocessing import cpu_count, Queue, Process, current_process
from netaddr import iprange_to_cidrs

# import local
import common

DB_NAME = common.DATAS_DIR + 'ripe.db.inetnum.gz'
NUM_WORKERS = cpu_count()


class Block:
    inetnum = ""
    netname = ""
    description = ""
    country = ""
    maintained_by = ""
    created = ""
    last_modified = ""

    def __init__(self, inetnum, netname, description, country, maintained_by, created, last_modified):
        self.inetnum = inetnum
        self.netname = netname
        self.description = description
        self.country = country
        self.maintained_by = maintained_by
        self.created = created
        self.last_modified = last_modified

    def __str__(self):
        return 'inetnum: {}, netname: {}, desc: {}, country: {}, maintained: {}, created: {}, updated: {}'.format(
            self.inetnum, self.netname, self.description, self.country,
            self.maintained_by, self.created, self.last_modified)

    def __repr__(self):
        return self.__str__()



def parse_property(block: str, name: str) -> str:
    match = re.findall(u'^{0:s}:\s*(.*)$'.format(name), block, re.MULTILINE)
    if match:
        return " ".join(match)
    else:
        return None


def parse_property_inetnum(block: str) -> str:
# IPv4
    match = re.findall('^inetnum:[\s]*((?:\d{1,3}\.){3}\d{1,3}[\s]*-[\s]*(?:\d{1,3}\.){3}\d{1,3})', block, re.MULTILINE)
    if match:
        ip_start = re.findall('^inetnum:[\s]*((?:\d{1,3}\.){3}\d{1,3})[\s]*-[\s]*(?:\d{1,3}\.){3}\d{1,3}', block, re.MULTILINE)[0]
        ip_end = re.findall('^inetnum:[\s]*(?:\d{1,3}\.){3}\d{1,3}[\s]*-[\s]*((?:\d{1,3}\.){3}\d{1,3})', block, re.MULTILINE)[0]
        cidrs = iprange_to_cidrs(ip_start, ip_end)
        return '{}'.format(cidrs[0])

def read_blocks(filename: str) -> list:
    f = gzip.open(filename, mode='rt', encoding='ISO-8859-1')
    single_block = ''
    blocks = []

    for line in f:
        if line.startswith('%') or line.startswith('#') or line.startswith('remarks:') or line.startswith(' '):
            continue
        # block end
        if line.strip() == '':
            if single_block.startswith('inetnum:') or single_block.startswith('inet6num:'):
                blocks.append(single_block)
                single_block = ''

            else:
                single_block = ''
        else:
            single_block += line

    f.close()

    return blocks

def parse_blocks(jobs: Queue):

    with open(common.FRENCH_PREFIXES_JSON, "a+") as f:
        while True:
            block = jobs.get()
            if block is None:
                break

            inetnum = parse_property_inetnum(block)
            netname = parse_property(block, 'netname')
            description = parse_property(block, 'descr')
            country = parse_property(block, 'country')
            maintained_by = parse_property(block, 'mnt-by')
            created = parse_property(block, 'created')
            last_modified = parse_property(block, 'last-modified')

            b = Block(inetnum=inetnum, netname=netname, description=description, country=country,
                      maintained_by=maintained_by, created=created, last_modified=last_modified)

            # only keep french IP and subnets bigger than /24
            # assuming smaller ones are admin and administrative stuff inside irr declarations
            if b.country == "FR" and ( int(b.inetnum.split('/')[1]) <= 24 ):
                f.write('"{0}":{{"name":"{1}"}},'.format(b.inetnum, b.netname))


def parse():

    if not os.path.isfile(DB_NAME):
        get_ripe_db()

    open(common.FRENCH_PREFIXES_JSON, "a+").write('{')

    blocks = read_blocks(DB_NAME)

    jobs = Queue()

    workers = []
    # start workers
    for w in range(NUM_WORKERS):
        p = Process(target=parse_blocks, args=(jobs,))
        p.start()
        workers.append(p)

    # add tasks
    for b in blocks:
        jobs.put(b)
    for i in range(NUM_WORKERS):
        jobs.put(None)

    # wait to finish
    for p in workers:
        p.join()


    open(common.FRENCH_PREFIXES_JSON, "a+").write('"end":{"end":"end"}}')

def get_ripe_db():
    url = "ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz"
    common.Affich.info(0, "Updating french prefixes from " + url)
    common.download(url, DB_NAME)
