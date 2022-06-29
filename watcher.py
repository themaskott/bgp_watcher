#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Project to set up a french prefixes watcher
Gather prefixes from internet routing registries (irr)
Parse several worldwide bgp collectors and search for hijacks on thoose prefixes

@Mk
14/06/2022
"""

# import from python
from os import path
import json, datetime, time
from netaddr import IPNetwork
# import local
import irr, rrc, autnums, common, subnets

# globals
FRENCH_PREFIXES = {}
AS_FR = {}


def history(collectors:list, ym:list)->dict:
    """
    Build an history for french prefixes announced in collectors during the month m of the year y
    Range : start day (sd) to end day (ed)
    """
    h = {}
    y,m=ym
    bviews=[]

    for c in collectors:
        for d in range(common.sd, common.ed):
            bviews.append(rrc.Bview(c, False,[y,m,d]))

    for b in bviews:
        b.get()
        common.Affich.success(1, "Downloading " + b.url)
        b.parse()
        common.Affich.success(1, "Parsing " + b.name)
        b.process()
        common.Affich.success(1, "Processing " + b.dump)
        for p in b.announced:
            if p in FRENCH_PREFIXES:
                if not p in h:
                    h.update({p:{}})
                for a in b.announced[p]:
                    if a in h[p]:
                        h[p][a] += 1
                    else:
                        h[p].update({a:1})

    # save history to file
    common.save_json_file( h, common.HISTORY_JSON )

    return h


def latest(collectors:list)->list:
    """
    Download and process latest bview from each collectors
    """
    # collectors from which parse bviews
    bviews = []

    common.Affich.success(0, "Checking latests bview")

    for c in collectors:
        bviews.append(rrc.Bview(c))

    for b in bviews:
        b.get()
        common.Affich.success(1, "Downloading " + b.url)
        b.parse()
        common.Affich.success(1, "Parsing " + b.name)
        b.process()
        common.Affich.success(1, "Processing " + b.dump)

    return bviews

def update(collectors:list)->list:
    """
    Download and process latest update from each collectors
    """
    updates = []

    for c in collectors:
        updates.append(rrc.Update(c))

    for u in updates:
        u.get()
        common.Affich.success(1, "Downloading " + u.url)
        u.parse()
        common.Affich.success(1, "Parsing " + u.name)
        u.process()
        common.Affich.success(1, "Processing " + u.dump)

    return updates

def search(collectors:list, ym:list)->dict:
    """
    Search latest for new announcment regarding history
    """

    y,m = ym
    if path.isfile( common.HISTORY_JSON ):
        common.Affich.success(0, "Loading existing history")
        h = common.load_json_file( common.HISTORY_JSON )
    else:
        common.Affich.success(0, "Building history")
        h = history(collectors, ym)

    bviews = latest(collectors)

    moas_json = {}
    country_json = {}

    # search for inconsistancies
    for b in bviews:
        for p in b.announced:
            # MOAS
            if p in FRENCH_PREFIXES and len(b.announced[p]) > 1:
                # print moas
                common.Affich.event(0, p,b.announced[p], "moas")
                # save to json
                if not p in moas_json:
                    moas_json.update({p:{"announced_by":b.announced[p]}})
                else:
                    for a in b.announced[p]:
                        if a not in moas_json[p]["announced_by"]:
                            moas_json[p]["announced_by"].append(a)

            # foreign AS announcing french prefix
            a = str(b.announced[p][0])
            if p in FRENCH_PREFIXES and not a in AS_FR:
                # prefix not seen in history
                if  not p in h:
                    country_json.update({p:{"announced_by":a, "tag":"new_p"}})
                    common.Affich.event(0, p,b.announced[p], "new_p")
                else:
                    # prefix previously seen but new AS announcer
                    if not b.announced[p][0] in h[p]:
                        country_json.update({p:{"announced_by":a, "tag":"new_a"}})
                        common.Affich.event(0, p,b.announced[p], "new_a")

                    # prefix and AS previously seen but few
                    elif h[p][b.announced[p][0]] < 2:
                        country_json.update({p:{"announced_by":a, "tag":"hijack"}})
                        common.Affich.event(0, p,b.announced[p], "hijack")

    # save JSON
    common.save_json_file(moas_json, common.MOAS_OUT_JSON )
    common.save_json_file(country_json, common.COUNTRY_OUT_JSON )

    return moas_json, country_json, h


def watch(moas_json:dict, country_json:dict, h:dict, collectors:list):
    """
    Monitor updates from given collectors
    """
    common.Affich.success(0, "Computing all FR subnets")
    all_fr_subnets = subnets.Subnets(FRENCH_PREFIXES).all_subnets()
    open(common.ALL_FR_SUBNETS_JSON,"w").write(str(all_fr_subnets))

    i = 1
    while i < common.count:

        common.Affich.success(0, "Update n°"+str(i))
        updates = update(collectors)

        for u in updates:
            for p in u.announced:
                if p in FRENCH_PREFIXES and len(u.announced[p]) > 1:
                    if p in moas_json:
                        common.Affich.event(0, p,u.announced[p], "knwon_moas")
                    else:
                        common.Affich.event(0, p,u.announced[p], "new_moas")
                        moas_json.update({p:{"announced_by":b.announced[p]}})

                a = str(u.announced[p][0])
                # prefix not seen in history
                if p in FRENCH_PREFIXES and not a in AS_FR:
                    if not p in h:
                        common.Affich.event(0, p,u.announced[p], "new_p")
                        country_json.update({p:{"announced_by":a, "tag":"new_p"}})
                    else:
                        if not u.announced[p][0] in h[p]:
                            common.Affich.event(0, p,u.announced[p], "new_a")
                            country_json.update({p:{"announced_by":a, "tag":"new_a"}})
                        elif h[p][u.announced[p][0]] < 2:
                            common.Affich.event(0, p,u.announced[p], "hijack")
                            country_json.update({p:{"announced_by":a, "tag":"hijack"}})


                if (a not in AS_FR) and (p not in FRENCH_PREFIXES) and (p in all_fr_subnets):
                    common.Affich.event(0, p,u.announced[p], "more_spec")


        # new update every 5 minutes
        time.sleep(300)
        i += 1

def main():
    # print menu
    if common.OUT: common.menu()

    # setup dir and filenames
    common.Affich.success(0, "Seting up env")
    common.setup()

    # create french_prefixes db if needed
    common.Affich.success(0, "Checking ripe.db.inetnum.gz")
    if not path.isfile( common.FRENCH_PREFIXES_JSON ):
        irr.parse()

    # create french_as db if needed
    common.Affich.success(0, "Checking french ASes db")
    if not path.isfile( common.FRENCH_AS_JSON ):
        autnums.extract_AS(autnums.update_AS())

    # load datas
    global FRENCH_PREFIXES, AS_FR
    FRENCH_PREFIXES = common.load_json_file( common.FRENCH_PREFIXES_JSON )
    AS_FR = common.load_json_file( common.FRENCH_AS_JSON )

    # first search from bview after building a history according to paramaters
    moas_json, country_json, h = search(common.collectors, common.ym)

    # watch updates announcements
    watch(moas_json, country_json, h, common.collectors)

if __name__ == "__main__":
    main()
