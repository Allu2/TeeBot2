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

import TeeBot, time, threading
from passwordi import password

bot = TeeBot.TeeBot("localhost", 9001, password) #use your own password here :P
con = bot.connect
bot.say("Connected.")
bot.writeLine("status")
check = 5
ticks = 0.2
while True:
    time.sleep(ticks)
    try:
        try:
            line = bot.readLine()
        except Exception as e:
            bot.debug("Error: " + e, "CRITICAL")
            exit()
            #	print line
        if b"[chat]:" in line.split(b" ")[0] and line.split(b" ")[1] != b"***":
            chat = bot.get_Chat(line)
            bot.debug("{0}: {1}".format(chat["Nick"].decode(), chat["Msg"].decode()), "CHAT")
        if b"[server]:" in line.split(b" ")[0] and b"client" in line.split(b" ")[1]:
            bot.debug("Player: {} has left the game.".format(bot.get_Leaves(line).decode()), "PLAYER")
            bot.writeLine("status")
        if b"[server]:" in line.split(b" ")[0] and (b"player" in line.split(b" ")[1] and b"has" in line.split(b" ")[2]):
            bot.writeLine("status")
        if b"[Server]: id=" in line:
            lista = bot.updTeeList(line)
        else:
            event = bot.get_Event(line)
            if event is not None:
                if event[-1] == "KILL" and event[-3] != b'-3':
                    bot.debug(event, "EVENT")
                    bot.debug("We got kill event.", "KILL")
                    bot.debug("Adding more to killers spree.", "KILL")
                    bot.debug("We got event:{}".format(event), "DEBUG")
                    try:
                        killer_tee = bot.get_Tee(event[0])
                    except (KeyError, NameError) as e:
                        bot.debug("Tee didn't exist! Updating playerlist!", "DEBUG")
                        bot.writeLine("status")
                    bot.debug("We got Tee:{}".format(killer_tee.get_nick()), "DEBUG")
                    killer_tee.set_spree(killer_tee.get_spree() + 1)
                    bot.debug("We have killer id: {}".format(event[0]), "DEBUG")
                    if killer_tee.get_idnum() == event[2]:
                        bot.debug("Its a suicide! reset killers stats!", "KILL")
                        killer_tee.set_spree(0)

                    else:
                        bot.debug("Resetting victims spree.", "KILL")
                        bot.debug(event[0], "DEBUG")
                        victim_tee = bot.get_Tee(event[2])
                        if victim_tee.get_spree() >= 5:
                            t = threading.Timer(5, bot.shutdown, args=[victim_tee, killer_tee])
                            t.start()

                        victim_tee.set_spree(0)
                        bot.killSpree(event[0])
                else:
                    pass
            else:
                pass
    except (KeyError, TypeError, AttributeError, NameError) as e:
        bot.debug("We got an error 1: {0}".format(e), "CRITICAL")
        bot.writeLine("status")
