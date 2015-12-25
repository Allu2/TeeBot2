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
from config import accesslog
from config import chatlog
from config import commands
import plugin_loader, logging, threading
logging.basicConfig()
logger = logging.getLogger("Bot")
logger.setLevel(logging.DEBUG)
bot = TeeBot.TeeBot(hostname, port, password) #Moved hostname, port and password to config file.

con = bot.connect
bot.say("Connected.")
bot.writeLine("status")
pl_loader = plugin_loader.Plugin_loader(bot)
bot.run()