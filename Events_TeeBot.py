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

        if line.split(b" ")[0] == b"[game]:":
            if b"[game]: kill killer='" in line: #Kill message
                result = re.search(b"kill killer='(\d+):(.+)' victim='(\d+):(.+)' weapon=([\d-]+) special=(\d+)", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append(
                    "KILL") #killer_id, killer_name, victim_id, victim_name, used_weapon_id, special(0/1(?)), type of event

                return lst
            if b"[game]: pickup " in line:
                result = re.search(b"pickup player='(\d+):(.+)' item=(\d+)/(\d+)", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append(self.Itemsolv(int(lst[2]), int(lst[3])))

                lst.append(
                    "PICKUP") #player_id, player_name, item_group(0 = hearts, 1 = armors,  2 = weapons(2/0=hammer 2/1 = pistol 2/2 = shotgun 2/3 = grenade 2/4 = rifle, 3 = special), group_id(useful for weapons (ninja 3/5)
                return lst
            if b"[game]: start " in line:
                "not implemented"
            if b"[game]: flag" in line:
                return ["FLAG"]
        else:
            return ["NONE"]

    def conversation(self, line):
        """
        ## conversation()
        Conversation is the function that handles chat messages and parses information from them.
        This information includes nick, the message, team id, player id and none which can be used to determine if message went to wrong location.
        if the information is correct "none" is False since we do have info
        if we got wrong "non chat" line we return none with value True, after all we have no info at all.
        """
        if line.split(b" ")[0] == b"[chat]:" and line.split(b" ")[1] != b"***":
        #	print "Works!"
        #	test = line.split(':') #test[0] =[chat], test[1] = id, test[2] =teamnumber, test[3] =nick, test[4] = message+\n
        #	name = test[3].lstrip(':')
        #	message_list = test[4:]
        #	message = ''.join(message_list).lstrip(': ').rstrip("\n")
        #	team = test[2].lstrip(':')
        #	ide = test[1].lstrip(" ")
            result = re.search(b"\[chat\]: (\d+):(-\d):(.+): (.+)", line)
            name = result.groups()[2]
            ide = result.groups()[0]
            message = result.groups()[-1]
            info = {"Nick": name, "Msg": message, "ID": ide}
            return info
        #[chat]: 0:-2:LeveL 5: moi
        else:
            info = {"none": "True"}
            return info

    def Weaponsolv(self, id):
        if id == -1:
            return "hit on a kill tile"
        if id == -2:
            return "kill command"
        if id == -3:
            return "leaving the game"
        if id == 0:
            return "pistol"
        if id == 1:
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
