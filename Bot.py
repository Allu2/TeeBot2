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
import time, importlib

import TeeBot
from config import password
from config import port
from config import hostname
from config import banned_nicks
from config import accesslog
from config import chatlog
from config import commands
import plugin_loader, logging
logging.getLogger("Bot")
logger = logging.basicConfig()

bot = TeeBot.TeeBot(hostname, port, password) #Moved hostname, port and password to config file.

con = bot.connect
bot.say("Connected.")
bot.writeLine("status")
pl_loader = plugin_loader.Plugin_loader(bot)
check = 5
ticks = 0

while True:
    time.sleep(ticks)
    try:
        try:
            line = bot.readLine()
            if line != b"\n":
                bot.debug(line, "RAW")
        except Exception as e:
            bot.debug("Error: " + repr(e), "CRITICAL")
            exit()
        if line == b"\n":
            pass
        elif b"[server]:" in line.split(b" ")[0] and (b"player" in line.split(b" ")[1] and b"has" in line.split(b" ")[2]):
            bot.writeLine("status")
        else:
            event = bot.get_Event(line)
            if event is not None:
                if event[-1] == "RELOAD ORDER":
                    bot.debug("Reloaded plugins", "DEBUG")
                    importlib.reload(plugin_loader)
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
                        nick = tee.get_nick()
                        ip = tee.get_ip()
                        time1 = time.strftime("%c", time.localtime())
                        accesslogi.write(
                            "[{}] ".format(time1) + "{} left the server ({})".format(nick.decode(), ip.decode()) + "\n")
                    bot.debug("{} has left the game.".format(bot.get_Leaves(event[0]).decode()), "PLAYER")
                    bot.writeLine("status")
                    tees = bot.player_count
                    if tees == 0:
                        bot.writeLine("restart")

                else:
                    pass
                if event[-1] == "UNKNOWN":
                    event = [line, "UNKNOWN"]
                pl_loader.event_handler(event)
            else:
                pass
    except (KeyError, TypeError, AttributeError, NameError, UnicodeDecodeError) as e:
        bot.debug("We got an error 1: {0}".format(e), "CRITICAL")
        bot.writeLine("status")