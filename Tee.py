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

import time


class Tee(object):
    def __init__(self, idnum, nick, ip, port, score, spree):
        self.nick = nick
        self.idnum = idnum
        self.ip = ip
        self.port = port
        self.score = score
        self.spree = spree
        self.largest_spree = 0
        #TODO: implement multikill messages. Catch each kills kill time, and reduce it from last. if the time we get is less then 3 seconds, add in to multikill.
        self.lastkilltime = 0
        self.multikill = 0
        self.largest_multikill = 0

    def get_spree(self):
        return self.spree

    def set_spree(self, spree):
        now = time.time()
        self.lastkilltime = now
        if spree > self.largest_spree:
            self.largest_spree = spree
        if now - self.lastkilltime <= 2:
            self.multikill += 1
        if now - self.lastkilltime > 2:
            self.multikill = 0

        if self.multikill > self.largest_multikill:
            self.largest_multikill = self.multikill
        self.spree = spree


    def get_nick(self):
        return self.nick

    def set_nick(self, nick):
        self.nick = nick

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def get_idnum(self):
        return self.idnum

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def set_multikill(self, multikill):
        self.multikill = multikill

    def get_multikill(self):
        return self.multikill

    def __str__(self):
        return ( str(self.nick) + ' comes from IP adress: ' + str(self.ip) + ':' + str(self.port) + ' and has player ID: ' + str(
            self.idnum) + ' and has ' + str(self.score) + ' points.')
