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

import time
import threading

import TeeBot
from config import password
from config import port
from config import hostname
from config import banned_nicks
from config import accesslog
from config import chatlog


bot = TeeBot.TeeBot(hostname, port, password) #Moved hostname, port and password to config file.
con = bot.connect
bot.say("Connected.")
bot.writeLine("status")
check = 5
ticks = 0
while True:
    time.sleep(ticks)
    try:
        try:
            line = bot.readLine()
            bot.debug(line, "RAW")
        except Exception as e:
            bot.debug("Error: " + e, "CRITICAL")
            exit()
        if b"[server]:" in line.split(b" ")[0] and (b"player" in line.split(b" ")[1] and b"has" in line.split(b" ")[2]):
            bot.writeLine("status")
        else:
            event = bot.get_Event(line)
            if event is not None:
                if event[-1] == "KILL" and event[-3] != b'-3':
                    # bot.debug("We got event: {}".format(event), "DEBUG")
                    try:
                        killer_tee = bot.get_Tee(event[0])
                    except (KeyError, NameError) as e:
                        bot.debug("Tee didn't exist! Updating player list!", "DEBUG")
                        bot.writeLine("status")
                    killer_tee.set_spree(killer_tee.get_spree() + 1)
                    if killer_tee.get_idnum() == event[2]:
                        killer_tee.set_spree(0)

                    else:
                        victim_tee = bot.get_Tee(event[2])
                        if victim_tee.get_spree() >= 5:
                            t = threading.Timer(5, bot.shutdown, args=[victim_tee, killer_tee, victim_tee.get_spree()])
                            t.start()

                        victim_tee.set_spree(0)
                        bot.killSpree(event[0])
                if event[-1] == "NICK CHANGE":
                    bot.writeLine("status")
                if event[-1] == "STATUS MESSAGE":
                    nick = event[3]
                    ide = event[0]
                    if nick.decode() in banned_nicks:
                        bot.writeLine("kick {0}".format(ide.decode()))
                    lista = bot.updTeeList(event)
                if event[-1] == "LEAVE":
                    with open(accesslog, "a", encoding="utf-8") as accesslogi:
                        tee = bot.get_Tee(event[0])
                        nick = tee.nick
                        ip = tee.ip
                        time1 = time.strftime("%c", time.localtime())
                        accesslogi.write(
                            "[{}] ".format(time1) + "{} left the server ({})".format(nick.decode(), ip.decode()) + "\n")
                    bot.debug("{} has left the game.".format(bot.get_Leaves(event[0]).decode()), "PLAYER")
                    bot.writeLine("status")
                    tees = len(bot.get_Teelista().keys())
                    if tees == 0:
                        bot.writeLine("restart")

                if event[-1] == "CHAT":
                    msg = event[1]
                    nick = event[0]
                    id = event[2]
                    with open(chatlog, "a", encoding="utf-8") as chatlogi:
                        time1 = time.strftime("%c", time.localtime())
                        chatlogi.write("[{}] ".format(time1) + "[{0}] ".format(nick.decode()) + msg.decode() + "\n")

                    if "/stats" == msg.decode():
                        tee = bot.get_Tee(id)
                        bot.say("Player: " + tee.get_nick().decode('utf-8'))
                        bot.say("Largest killing spree: " + str(tee.largest_spree))
                        bot.say("Largest multikill: " + str(tee.largest_multikill))
                        bot.say("Total kills: " + str(tee.kills))
                    if "/pause" == msg.decode():
                        bot.say("One does not simply pause an online game!")
                else:
                    pass
            else:
                pass
    except (KeyError, TypeError, AttributeError, NameError) as e:
        bot.debug("We got an error 1: {0}".format(e), "CRITICAL")
        bot.writeLine("status")
