#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import from python
import json
from netaddr import IPNetwork

# import local
import common

class Subnets():
    """
    Given a dict of prefixes, compute all subnets for each prefix
    With mask lower than 24, assuming greater masks are not announced through BGP
    """
    prefixes = {}

    def __init__(self, prefixes:dict):
        self.prefixes = prefixes

    def all_subnets(self):
        s = set()
        for p in self.prefixes:
            try:
                ip = IPNetwork(p)
                len = ip.prefixlen
            except:
                pass
            if ip.version == 4 and len <= 24:
                for mask in range(len, 25):
                    s.update([str(_) for _ in ip.subnet(mask)])
        return s
