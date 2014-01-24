#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2013 Aleksi Joakim Palomäki <aleksi@Oblivion>
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

import Tees, telnetlib, Events_TeeBot, re


class TeeBot(object):
    def __init__(self, host, port, passwd):
        self.passwd = passwd
        self.host = host
        self.port = port
        self.address = host + ":" + str(port)
        self.teelst = Tees.Tees()
        self.events = Events_TeeBot.Events()

    @property
    def connect(self):
        self.tn = telnetlib.Telnet(self.host, self.port)
        self.tn.read_until(b"Enter password:\n")
        self.tn.write(str(self.passwd).encode('utf-8') + b'\n')
        return self.tn

    def readLine(self):
        return self.tn.read_until(b"\n")

    def writeLine(self, line):
        self.tn.write(str(line).encode('utf-8') + b"\n")

    def readLines(self, until):
        return self.tn.read_until(str(until).encode('utf-8'), 0.6)

    def say(self, message):
        self.writeLine('say "TeeBot: ' + message.replace('"', "'") + "\"'")

    def brd(self, message):
        self.writeLine('broadcast "' + message.replace('"', "'") + "\"'")

    def get_Teelista(self):
        return self.teelst.get_TeeLst()

    def updTeeList(self, line):
        if b"[Server]: id=" in line:
            result = re.search(b"id=(\d+) addr=(.+):(\d+) name='(.+)' score=(.+)", line)
            print(result.groups())
            for x in result.groups():
                print(x)
            self.teelst.add_Tee(result.groups()[0], result.groups()[3], result.groups()[1], result.groups()[2],
                                result.groups()[-1], 0) # id, name, ip, port, score
        return self.teelst.get_TeeLst()

    def get_Leaves(self, line):
        if b"[server]: client dropped. cid=" in line:
            result = re.search("\[server\]: client dropped. cid=(\d+)", line)
            print(result.groups()[0])
            ide = result.groups()[0]
            nick = self.teelst.get_Tee(ide).nick
            self.teelst.rm_Tee(ide)
            return nick

    def get_Chat(self, line):
        return self.events.conversation(line)

    def get_Event(self, line):
        return self.events.game_events(line)

