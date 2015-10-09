#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       Author: Aleksi Palomäki, a.k.a Allu2 <aleksi.ajp@gmail.com>
#        Copyright: GPL3 2011
#
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import time, json
#from Plugins import ai


class Tee(object):
    def __init__(self, idnum, nick, ip, port, score, spree):

        self.attributes = {"nick": nick,
                           "id": int(idnum),
                           "ip": ip,
                           "port": port,
                           "score": score,
                           "spree": spree,
                           "largest_spree": 0,
                           "multikill": 1,
                           "largest_multikill": 0,
                           "kills": 0,
                           "team": None}

    def get_spree(self):
        return self.attributes["spree"]

    def set_spree(self, spree):
        now = time.time()
        if spree > 0:
            if spree > self.attributes["largest_spree"]:
                self.attributes["largest_spree"] = spree
            if now - self.lastkilltime <= 2:
                self.attributes["multikill"] += 1
            if now - self.lastkilltime > 2:
                self.attributes["multikill"] = 1

            if self.attributes["multikill"] > self.attributes["largest_multikill"]:
                self.set_largest_multikill(self.attributes["multikill"])

            self.lastkilltime = now
        self.attributes["spree"] = spree
        self.attributes["kills"] += 1
    def get_idnum(self):
        return self.attributes["idnum"]

    def set_idnum(self, idnum):
        self.attributes["idnum"] = int(idnum)

    def get_nick(self):
        return self.attributes["nick"]

    def set_nick(self, nick):
        self.attributes["nick"] = nick

    def get_ip(self):
        return self.attributes["ip"]

    def set_ip(self, ip):
        self.attributes["ip"] = ip

    def get_port(self):
        return self.attributes["port"]

    def set_port(self, port):
        self.attributes["port"] = port

    def get_idnum(self):
        return self.attributes["idnum"]

    def get_score(self):
        return self.attributes["score"]

    def set_score(self, score):
        self.attributes["score"] = score

    def set_multikill(self, multikill):
        self.attributes["multikill"] = multikill

    def get_multikill(self):
        return self.attributes["multikill"]

    def get_largest_spree(self):
        return self.attributes["largest_spree"]

    def get_largest_multikill(self):
        return self.attributes["largest_multikill"]

    def set_largest_multikill(self, largest_multikill):
        self.attributes["largest_multikill"] = largest_multikill

    @property
    def tojson(self):
        return json.dumps(self.attributes, indent=3)

    def __str__(self):
        return ( str(self.attributes["nick"]) + ' comes from IP adress: ' + str(self.attributes["ip"]) + ':' + str(self.attributes["port"]) + ' and has player ID: ' + str(
            self.attributes["idnum"]) + ' and has ' + str(self.attributes["score"]) + ' points.')
