# -*- coding: utf-8 -*-
#       Author: Aleksi Palomäki, a.k.a Allu2 <aleksi.ajp@gmail.com>
#        Copyright: GPL3 2011
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       


#Some notes
"""
Ok so this is a "class" that is suppose to handle some events that occur on teeworlds server.
So far it supports parsing conversation (and for a server-side bot i think this is crucial)
It also supports somehow ripping information from "status" command in order to get statistic and player info
With some introduction of regexp and stuff this documentation should be redone.
"""
import re


class Events():
    def msg_found(self, msg, message):
        """
        ## msg_found()
        msg_found() is quite self explanatory,
        It takes two arguments "msg" and "message"
        "msg" is the string you search in "message"
        if msg is found in the message it returns True, if not False.
        """
        if msg in message:
            return True
        else:
            return False

    def game_events(self, line):
        import re

        splitted_line = line.split(b" ")

        #TODO: Broadcast messages, say messages, votes...
        if splitted_line[0] == b"[game]:":
            if splitted_line[1] == b"kill" and (b"killer=" in splitted_line[2]):
                # if b"[game]: kill killer='" in line: #Kill message
                result = re.search(b"kill killer='(\d+):(.+)' victim='(\d+):(.+)' weapon=([\d-]+) special=(\d+)", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append(
                    "KILL") #killer_id, killer_name, victim_id, victim_name, used_weapon_id, special(0/1(?)), type of event

                return lst
            if splitted_line[1] == b"pickup":
                # if b"[game]: pickup " in line:
                result = re.search(b"pickup player='(\d+):(.+)' item=(\d+)/(\d+)", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append(self.Itemsolv(int(lst[2]), int(lst[3])))

                lst.append(
                    "PICKUP") #player_id, player_name, item_group(0 = hearts, 1 = armors,  2 = weapons(2/0=hammer 2/1 = pistol 2/2 = shotgun 2/3 = grenade 2/4 = rifle, 3 = special), group_id(useful for weapons (ninja 3/5)
                return lst
            # [game]: start round type='CTF' teamplay='1'
            if splitted_line[1] == b"start":
                result = re.search(b"start round type='(.+)' teamplay='(\d+)'", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append("START")
                return lst
            if splitted_line[1] == b"flag_grab":
                # if b"[game]: flag_grab" in line: #flag_grab player='2:Lauti super'
                result = re.search(b"flag_grab player='(\d+):(.+)'", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append("FLAG") #player_id, player_name, type of event
                return lst
            if splitted_line[1] == b"flag_capture":
                #if b"[game]: flag_capture" in line:
                result = re.search(b"flag_capture player='(\d+):(.+)'", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append("CAPTURE") #player_id, player_name, type of event
                return lst
        if splitted_line[0] == b"[chat]:":
            if splitted_line[1] != b"***":
                lst = self.conversation(line)
                if lst[-1] != "NONE":
                    lst.append("CHAT")
                else:
                    lst.append("UNKNOWN")
                return lst
            if splitted_line[1] == b"***":
                if b"' changed name to '" in line:
                    result = re.search(b"'(.+)' changed name to '(.+)'", line)
                    lst = list(result.groups())  # old, new
                    lst.append("NICK CHANGE")
                    return lst
                else:
                    return ["SERVER SAY"]
        if splitted_line[0] == b"[Console]:":
            if b"!reload" in line:
                return ["RELOAD ORDER"]
            else:
                return ["CONSOLE MESSAGE"]
        if (splitted_line[0] == b"[Server]:" and (b"id=" in splitted_line[1])) and splitted_line[-1] != b"connecting\n":
            result = re.search(b"id=(\d+) addr=(.+):(\d+) name='(.+)' score=(.+)", line)
            lst = list(result.groups())
            lst.append("STATUS MESSAGE")
            return lst  # id, ip, port, nick, score, event type
        if splitted_line[0] == b"[server]:":
            if splitted_line[1] == b"client":
                result = re.search(b"\[server\]: client dropped. cid=(\d+)", line)
                ide = list(result.groups())
                ide.append("LEAVE")
                return ide
            if b"cid=" in splitted_line[1] or b"ClientID=" in splitted_line[1]:
                return ["COMMAND"]
            if splitted_line[1] == b"player":
                return ["CONNECTING"]
            else:
                return ["UNKNOWN"]
        else:
            return ["UNKNOWN"]
            #b'[Console]: hei\n'

    def conversation(self, line):
        """
        ## conversation()
        Conversation is the function that handles chat messages and parses information from them.
        This information includes nick, the message, team id, player id and none which can be used to determine if message went to wrong location.
        if the information is correct "none" is False since we do have info
        if we got wrong "non chat" line we return none with value True, after all we have no info at all.
        """
        if line.split(b" ")[0] == b"[chat]:" and line.split(b" ")[1] != b"***":
            result = re.search(b"\[chat\]: (\d+):(-\d):(.+): (.+)", line)
            name = result.groups()[2]
            ide = result.groups()[0]
            message = result.groups()[-1]
            info = [name, message, ide]
            return info
        #[chat]: 0:-2:LeveL 5: mo
        else:
            info = ["NONE", "NONE", "NONE"]
            return info

    def Weaponsolv(self, id):
        if id == -1:
            return "hit on a kill tile"
        if id == -2:
            return "kill command"
        if id == -3:
            return "changing team/leaving"
        if id == 1:
            return "pistol"
        if id == 0:
            return "hammer"
        if id == 2:
            return "shotgun"
        if id == 3:
            return "grenade"
        if id == 4:
            return "rifle"

        else:
            return "something magical.."

    def Itemsolv(self, id1, id2):
        if id1 > 1:
            return self.Weaponsolv(id2)
        if id1 == 0:
            return "heart"
        if id1 == 1:
            return "armor"
        else:
            return "something magical.."
