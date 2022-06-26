#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import from python
import requests, json
from html.parser import HTMLParser
import typing

# import local
import common

class MyHTMLParser(HTMLParser):
    """
    HTML parser for https://www.cidr-report.org/as2.0/autnums.html
    Feeds AS dictionnary with {AS number : { "organisation" : AS full name, "country" : AS country }}
    Here only if country == FR
    """
    isASNum = False
    isASName = False
    ASNum = ""
    ASName = ""
    ASCountry = ""
    AS = {}

    def handle_starttag(self, tag, attrs):
        if tag == "a": self.isASNum = True

    def handle_endtag(self, tag):
        if tag == "a": self.isASName = True

    def handle_data(self, data):
        if self.isASNum:
            self.ASNum = data.strip()
            self.ASNum = int(self.ASNum[2:])
            self.isASNum = False
        elif self.isASName:
            l = data.replace("\n","").strip()
            self.ASName = " ".join(l.split(",")[0:-1])
            self.ASCountry = l.split(",")[-1].strip()
            # extract only french ASes
            if self.ASCountry == "FR" or (self.ASCountry == "EU" and self.ASName.startswith("FR-")):
                self.AS.update({self.ASNum : {"organisation" : self.ASName, "country" : self.ASCountry}})
            self.isASName = False

def update_AS()->str:
    """
    Get last update of AS number - AS names
    """
    url = "https://www.cidr-report.org/as2.0/autnums.html"
    common.Affich.info(0, "Updating french ASes from " + url)
    r = requests.get(url, verify=False)
    return r.content.decode()


def extract_AS(source:str):
    """
    Apply parser to input
    """
    parser = MyHTMLParser()
    parser.feed(source)

    # save to file
    common.save_json_file( parser.AS, common.FRENCH_AS_JSON )
