#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RRC00 	Amsterdam, NL  	 multihop 	global
RRC01 	London, GB 	     IXP 	LINX, LONAP
RRC03 	Amsterdam, NL 	 IXP 	AMS-IX, NL-IX
RRC04 	Geneva, CH 	     IXP 	CIXP
RRC05 	Vienna, AT 	     IXP 	VIXP
RRC06 	Otemachi, JP 	 IXP 	DIX-IE
RRC07 	Stockholm, SE    IXP 	Netnod
RRC10 	Milan, IT 	     IXP 	MIX
RRC11 	New York, US     IXP 	NYIIX
RRC12 	Frankfurt, DE 	 IXP 	DE-CIX
RRC13 	Moscow, RU 	     IXP 	MSK-IX
RRC14 	Palo Alto,       US 	IXP 	PAIX
RRC15 	Sao Paolo, BR 	 IXP 	PTTMetro-SP
RRC16 	Miami, FL, US 	 IXP 	Equinix Miami
RRC18 	Barcelona, ES 	 IXP 	CATNIX
RRC19 	Johannesburg, ZA IXP 	NAP Africa JB
RRC20 	Zurich, CH 	     IXP 	SwissIX
RRC21 	Paris, FR 	     IXP 	France-IX Paris and France-IX Marseille)
RRC22 	Bucharest, RO 	 IXP 	Interlan
RRC23 	Singapore, SG 	 IXP 	Equinix Singapore
RRC24 	Montevideo, UY 	 multihop 	LACNIC region
RRC25 	Amsterdam, NL 	 multihop 	global
RRC26 	Dubai, AE 	     IXP 	UAE-IX
"""

# import from python
import wget, datetime, subprocess
from os import path, remove

# import local
import common

class Bview():
    rrc = 0
    latest = True
    url = ""
    name = ""
    dump = ""
    announced = {}

    def __init__(self, rrc, latest=True, ymd=[2022,5,1]):
        self.rrc = rrc
        self.latest = latest
        if latest:
            self.url = "https://data.ris.ripe.net/rrc{:02n}/latest-bview.gz".format(self.rrc)
            self.name = common.SESSION_DIR + "{}-rrc{:02n}-bview.gz".format(datetime.date.today(), self.rrc)
            self.dump = common.SESSION_DIR + "{}-rrc{:02n}-dump.txt".format(datetime.date.today(), self.rrc)
        else:
            # 3 bviews per day : 00h00, 08h00 and 16h00
            # using the 08h00 one
            y,m,d=ymd
            self.url = "https://data.ris.ripe.net/rrc{:02n}/{:04n}.{:02n}/bview.{:04n}{:02n}{:02n}.0800.gz".format(self.rrc, y, m, y, m, d)
            self.name = common.SESSION_DIR + "{:04n}-{:02n}-{:02n}-rrc{:02n}-bview.gz".format(y,m,d, self.rrc)
            self.dump = common.SESSION_DIR + "{:04n}-{:02n}-{:02n}-rrc{:02n}-dump.txt".format(y,m,d, self.rrc)

    def get(self):
        """
        Download and save the bview
        """
        if not path.isfile(self.name): common.download(self.url, self.name)

    def parse(self):
        """
        Parse the bview using bgpdump into text file legacy format
        """
        if not path.isfile(self.dump): subprocess.run(["./bgpdump", "-M", "-O", self.dump, self.name], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT )

    def process(self):
        """
        Parse the text dumped file to extract announced prefix and announcer AS
        """
        with open(self.dump,"r") as f:
            for l in f:
                prefix = l.split('|')[5]
                announcer = l.split('|')[6].split(' ')[-1]
                if prefix in self.announced:
                    if announcer not in self.announced[prefix]:
                        self.announced[prefix].append(announcer)
                else:
                    self.announced.update({prefix:[announcer]})


class Update():
    rrc = 0
    latest = True
    url = ""
    name = ""
    dump = ""
    announced = {}

    def __init__(self, rrc, latest=True, ymd=[2022,5,1]):
        self.rrc = rrc
        self.latest = latest
        if latest:
            self.url = "https://data.ris.ripe.net/rrc{:02n}/latest-update.gz".format(self.rrc)
            self.name = common.SESSION_DIR + "{}-rrc{:02n}-update.gz".format(datetime.date.today(), self.rrc)
            self.dump = common.SESSION_DIR + "{}-rrc{:02n}-update-dump.txt".format(datetime.date.today(), self.rrc)
        #else:
        #not implemanted


    def get(self):
        """
        Download and save the update
        """
        if path.isfile(self.name): remove(self.name)
        common.download(self.url, self.name)

    def parse(self):
        """
        Parse the update using bgpdump into text file legacy format
        """
        if path.isfile(self.dump): remove(self.dump)
        subprocess.run(["./bgpdump", "-M", "-O", self.dump, self.name], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT )

    def process(self):
        """
        Parse the text dumped file to extract announced prefix and announcer AS
        """
        with open(self.dump,"r") as f:
            for l in f:
                type = l.split('|')[2]
                # announce type A = ADD
                # announce type W = WITHDRAW
                if type == "A":
                    prefix = l.split('|')[5]
                    announcer = l.split('|')[6].split(' ')[-1]
                    if prefix in self.announced:
                        if announcer not in self.announced[prefix]:
                            self.announced[prefix].append(announcer)
                    else:
                        self.announced.update({prefix:[announcer]})
