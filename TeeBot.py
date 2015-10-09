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

import telnetlib
import time, logging

import Tees
import Events_TeeBot
from config import accesslog
from config import nick

class TeeBot(object):
    def __init__(self, host, port, passwd):
        self.passwd = passwd
        self.host = host
        self.port = port
        self.address = host + ":" + str(port)
        self.teelst = Tees.Tees()
        self.events = Events_TeeBot.Events()
        self.name = nick
        self.logger = logging.getLogger("Bot")
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.exception = self.logger.exception

    @property
    def player_count(self):
        return len(self.teelst.get_TeeLst().keys())

    @property
    def connect(self):
        self.debug("Connecting to server..")
        self.tn = telnetlib.Telnet(self.host, self.port)
        self.debug("Telnet Object created.")
        lines = self.tn.read_until(b"Enter password:")
        self.tn.write(str(self.passwd).encode('utf-8') + b'\n')
        return self.tn

    def talk(self, msg, method):
        #self.logger.debug(msg)
        if method == "game_chat":
            self.say(msg)
        elif method == "terminal":
            pass
        else:
            pass

    def readLine(self):
        return self.tn.read_until(b"\n")

    def writeLine(self, line):
        self.tn.write(str(line).encode('utf-8') + b"\n")

    def readLines(self, until):
        return self.tn.read_until(str(until).encode('utf-8'), 0.6)

    def echo(self, message):
        self.debug("Echoing: {}".format(message))
        self.writeLine('echo "'+self.name+': ' + message.replace('"', "'") + "\"'")

    def say(self, message):
        self.debug("Saying: {}".format(message))
        self.writeLine('say "'+self.name+': ' + message.replace('"', "'") + "\"'")

    def brd(self, message):
        self.debug("Broadcating: {}".format(message))
        self.writeLine('broadcast "' + message.replace('"', "'") + "\"'")

    def killSpree(self, id):
        tee = self.get_Teelista().get(id)
        spree = tee.get_spree()
        if (spree % 5) == 0 and spree != 0:
            msg = tee.get_nick().decode('utf-8') + " is on a killing spree with " + str(tee.get_spree()) + " kills!"
            self.brd(msg)
            pass
    def Multikill(self, id):
        tee = self.get_Teelista().get(id)
        multikill = tee.get_multikill()
        if multikill>=2:
            if multikill == 2:
                self.brd(tee.get_nick().decode('utf-8') + " DOUBLEKILL!")
                pass
            if multikill == 3:
                self.brd(tee.get_nick().decode('utf-8') + " TRIPLEKILL!")
                pass
            if multikill == 4:
                self.brd(tee.get_nick().decode('utf-8') + " QUODRAKILL!!")
                pass
            if multikill == 5:
                self.brd(tee.get_nick().decode('utf-8') + " PENTAKILL!")
                pass
            if multikill >=6:
                self.brd(tee.get_nick().decode('utf-8') + " IS A BADASS!")
                self.writeLine("pause")
                self.say("Alright stop, everybody stop!")
                time.sleep(1)
                self.say("Someone just killed over 5 people in a multikill..")
                time.sleep(2)
                self.say("That was damn AMAZING!")
                time.sleep(2)
                self.say("Damn.. Ok guys, continue, just had to take a moment to point out this epic achievement.")
                self.writeLine("pause")
            else:
                pass
        else:
            pass
    def shutdown(self, victim_tee, killer_tee, spree):
        self.brd(
            "{0}'s {2} kill spree was shutdown by {1}!".format(victim_tee.get_nick().decode(),
                                                                         killer_tee.get_nick().decode(), str(spree)))

    def get_Teelista(self):
        return self.teelst.get_TeeLst()

    def get_Tee(self, id):
        return self.teelst.get_Tee(int(id))

    def updTeeList(self, event):

        # try:
        # self.debug(result.groups(), "DEBUG")
        # if result.groups()[3].decode() in banned_nicks:
        #         self.writeLine("kick {0}".format(result.groups()[0].decode()))
        #
        # except AttributeError as e:
        #     self.debug("Error: {0}".format(e), "CRITICAL")
        try:
            tee = self.teelst.get_Tee(event[0])
            if tee.get_nick().decode() != event[3].decode():
                old_ip = tee.get_ip()
                tee.set_nick(event[3])
                tee.set_score(event[4])
                tee.set_ip(event[1])
                tee.set_port(event[2])
                if old_ip != tee.get_ip():
                    with open(accesslog, "a", encoding="utf-8") as accesslogi:
                        time1 = time.strftime("%c", time.localtime())
                        accesslogi.write("[{}] ".format(time1) + "{} joined the server ({})".format(tee.get_nick().decode(),
                                                                                                    tee.get_ip().decode()) + "\n")
                else:
                    pass
        except AttributeError as e:
            self.exception(e)
        except KeyError as e:
            self.debug("Didn't find Tee: {} in player lists, adding it now:".format(event[3].decode()))
            self.exception(e)
            with open(accesslog, "a", encoding="utf-8") as accesslogi:
                nick = event[3]
                ip = event[1]
                time1 = time.strftime("%c", time.localtime())
                accesslogi.write(
                    "[{}] ".format(time1) + "{} joined the server ({})".format(nick.decode(), ip.decode()) + "\n")
            self.teelst.add_Tee(event[0], event[3], event[1], event[2],
                                event[-1], 0)  # id, name, ip, port, score
        return self.teelst.get_TeeLst()

    def get_Leaves(self, ide):
        nick = self.teelst.get_Tee(ide).get_nick()
        self.teelst.rm_Tee(ide)
        return nick

    def get_Chat(self, line):
        return self.events.conversation(line)

    def get_Event(self, line):

        lst = self.events.game_events(line)

        # if lst is not None:
        # if lst[-1] == "KILL":
        # self.debug(
        #             "Player " + lst[3].decode() + " was killed by " + lst[
        #                 1].decode() + " with a " + self.events.Weaponsolv(
        #                 int(lst[4])), "KILL")
        #         return lst
        #     if lst[-1] == "PICKUP":
        #         self.debug(lst[-2] + " was picked up by " + lst[1].decode(), "INFO")
        #         return lst
        #     if lst[-1] == "FLAG":
        #         self.debug("Flag was grabbed by " + lst[1].decode(), "FLAG")
        #     if lst[-1] == "CAPTURE":
        #         self.debug("Flag was Captured by " + lst[1].decode(), "FLAG")
        #TODO: Broadcast messages, say messages, votes...
        if lst[-1] != "UNKNOWN":
            self.debug("Following event occured: {}".format(lst[-1]))
        return lst




