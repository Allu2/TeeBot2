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

import TeeBot
from passwordi import password

bot = TeeBot.TeeBot("localhost", 9001, password) #use your own password here :P
con = bot.connect
bot.say("Connected.")
bot.writeLine("status")
check = 5
while True:
    try:
        try:
            line = bot.readLine()
        except Exception as e:
            bot.events.debug("Error: " + e, "SEVERE")
            exit()
            #	print line
        if b"[chat]:" in line.split(b" ")[0] and line.split(b" ")[1] != b"***":
            chat = bot.get_Chat(line)
            print((chat["Nick"] + b": " + chat["Msg"]))
            try:
                lista = bot.get_Teelista()
                for x in lista:
                    bot.say(lista[x].get_nick())
            except:
                print("Couldn't list players, some error!")
            #	print chat
        if b"[server]:" in line.split(b" ")[0] and b"client" in line.split(b" ")[1]:
            bot.events.debug((bot.get_Leaves(line)))
            bot.writeLine("status")
        if b"[server]:" in line.split(b" ")[0] and (b"player" in line.split(b" ")[1] and b"has" in line.split(b" ")[2]):
            bot.writeLine("status")
        if b"[Server]: id=" in line:
            lista = bot.updTeeList(line)
        else:
            event = bot.get_Event(line)
            if event[-1] == "KILL":
                bot.events.debug(event, "EVENT")
                bot.events.debug("We got kill event.", "KILL")
                bot.events.debug("Adding more to killers spree.", "KILL")
                killer_tee = bot.get_Teelista().get(event[2])
                killer_tee.set_spree(killer_tee.get_spree() + 1)
                bot.events.debug("We have killer id: {}".format(event[2]), "DEBUG")
                if killer_tee.get_idnum() == event[0]:
                    bot.events.debug("Its a suecide! reset killers stats!", "KILL")
                    killer_tee.set_spree(0)

                else:
                    bot.events.debug("Resetting victims spree.", "KILL")
                    bot.events.debug(event[0], "DEBUG")
                    victim_tee = bot.get_Teelista().get(event[0])
                    victim_tee.set_spree(0)
                    bot.killSpree(event[2])
            else:
                pass
    except (KeyError, TypeError, AttributeError) as e:
        bot.events.debug("We got an error: {0}".format(e), "CRITICAL")
        bot.writeLine("status")
