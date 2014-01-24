#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       Author: Aleksi Palomäki, a.k.a Allu2 <aleksi.ajp@gmail.com>
#        Copyright: GPL3 2011
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
import Tee


class Tees(object):
    def __init__(self):
        self.teelst = {}

    def add_Tee(self, idnum, nick, ip, port, score, spree):
        tee = Tee.Tee(idnum, nick, ip, port, score, spree)
        self.teelst[tee.idnum] = tee

    def get_Tee(self, player_id):
        return self.teelst[player_id]

    def rm_Tee(self, player_id):
        del self.teelst[player_id]

    def rm_Tee_all(self):
        self.teelst = {}

    def get_TeeLst(self):
        return self.teelst

		
