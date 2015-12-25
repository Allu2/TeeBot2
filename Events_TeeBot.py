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
import time
import logging
logger = logging.getLogger("Bot")
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
        splitted_line = line.split(" ")
        #TODO: Broadcast messages, say messages, votes...
        if splitted_line[0] == "[game]:":
            if splitted_line[1] == "kill" and ("killer=" in splitted_line[2]):
                # if "[game]: kill killer='" in line: #Kill message
                result = re.search("kill killer='(\d+):(.+)' victim='(\d+):(.+)' weapon=([\d-]+) special=(\d+)", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append(
                    "KILL") #killer_id, killer_name, victim_id, victim_name, used_weapon_id, special(0/1(?)), type of event
                reply_dictionary = \
                    {
                        "event_type": "KILL",
                        "killer_id":        lst[0],
                        "killer_name":      lst[1],
                        "victim_id":        lst[2],
                        "victim_name":      lst[3],
                        "user_weapon_id":   lst[4],
                        "special":          lst[5],
                        "time_stamp":       time.time(),
                }

                return reply_dictionary
            if splitted_line[1] == "pickup":
                # if "[game]: pickup " in line:
                result = re.search("pickup player='(\d+):(.+)' item=(\d+)/(\d+)", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append(self.Itemsolv(int(lst[2]), int(lst[3])))

                lst.append(
                    "PICKUP") #player_id, player_name, item_group(0 = hearts, 1 = armors,  2 = weapons(2/0=hammer 2/1 = pistol 2/2 = shotgun 2/3 = grenade 2/4 = rifle, 3 = special), group_id(useful for weapons (ninja 3/5)
                reply_dictionary = \
                    {
                        "event_type": "PICKUP",
                        "player_id":        lst[0],
                        "player_name":      lst[1],
                        "item_group":       lst[2],
                        "group_id":         lst[3],
                        "name":             lst[-2],
                        "time_stamp":       time.time(),
                }
                return reply_dictionary
            # [game]: start round type='CTF' teamplay='1'

            if splitted_line[1] == "start":
                result = re.search("start round type='(.+)' teamplay='(\d+)'", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append("START")
                reply_dictionary = \
                    {
                        "event_type": "START",
                        "game_type":        lst[0],
                        "team_game":        lst[1],
                        "time_stamp":       time.time(),
                    }
                return reply_dictionary

            if splitted_line[1] == "flag_gra":
                # if "[game]: flag_gra" in line: #flag_grab player='2:Lauti super'
                result = re.search("flag_grab player='(\d+):(.+)'", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append("FLAG") #player_id, player_name, type of event
                reply_dictionary = \
                    {
                        "event_type":       "FLAG",
                        "player_id":        lst[0],
                        "player_name":      lst[1],
                        "time_stamp":       time.time(),
                    }
                return reply_dictionary

            if splitted_line[1] == "flag_capture":
                #if "[game]: flag_capture" in line:
                result = re.search("flag_capture player='(\d+):(.+)'", line)
                groups = result.groups()
                lst = list(result.groups())
                lst.append("CAPTURE") #player_id, player_name, type of event
                reply_dictionary = \
                    {
                        "event_type":       "CAPTURE",
                        "player_id":        lst[0],
                        "player_name":      lst[1],
                        "time_stamp":       time.time(),
                    }
                return lst

            if splitted_line[1] == "team_join":
                # "[game]: team_join player='0:LeveL 6' team=0\n"
                result = re.search("team_join player='(\d+):(.+)'", line)
                groups = result.groups()
                lst = list(result.groups())
                moved = False
                line = line
                if "m_Team=" in line.split(" ")[-1]:
                    moved = True
                print("möh")
                lst.append(line.split(" ")[-1].replace("m_Team=", "").replace("team=", "").replace("\\n", "").replace("b'", "").replace("'", ""))
                lst.append(moved)
                lst.append("TEAM_JOIN")
                reply_dictionary = \
                    {
                        "event_type":       "TEAM_JOIN",
                        "player_id":        lst[0],
                        "player_name":      lst[1],
                        "changed_team":     moved,
                        "time_stamp":       time.time(),
                    }
                return reply_dictionary

        if (line.split(" ")[0] == "[chat]:" or line.split(" ")[0] == "[teamchat]:"):
            if splitted_line[1] != "***":
                if "[teamchat]" in line.split(" ")[0]:
                    lst = self.conversation(line, True)
                else:
                    lst = self.conversation(line, False)
                if lst[-1] != "NONE":
                    if "[teamchat]" in line.split(" ")[0]:
                        lst.append("TEAMCHAT")
                    else:
                        lst.append("CHAT")
                else:
                    lst.append("UNKNOWN")
                reply_dictionary = \
                    {
                        "event_type":       lst[-1],
                        "player_name":      lst[0],
                        "message":          lst[1],
                        "player_id":        lst[2],
                        "time_stamp":       time.time(),
                    }
                return reply_dictionary
            if splitted_line[1] == "***":
                if "' changed name to '" in line:
                    result = re.search("'(.+)' changed name to '(.+)'", line)
                    lst = list(result.groups())  # old, new
                    lst.append("NICK_CHANGE")
                    reply_dictionary = \
                        {
                            "event_type":       lst[-1],
                            "old_name":         lst[0],
                            "new_name":         lst[1],
                            "time_stamp":       time.time(),
                        }

                    return reply_dictionary
                else:
                    return {"event_type": "SERVER SAY", "time_stamp": time.time()}

        if splitted_line[0] == "[Console]:":
            if "!reload" in line:
                return {"event_type": "RELOAD_ORDER", "time_stamp": time.time()}
            else:
                return {"message": splitted_line[1], "event_type": "CONSOLE_MESSAGE", "time_stamp": time.time()}

        if (splitted_line[0] == "[Server]:" and ("id=" in splitted_line[1])) and splitted_line[-1] != "connecting\n":
            result = re.search("id=(\d+) addr=(.+):(\d+) name='(.+)' score=(.+)", line)
            lst = list(result.groups())
            lst.append("STATUS_MESSAGE")
            reply_dictionary = \
                {
                    "event_type":       lst[-1],
                    "player_id":        lst[0],
                    "ip":               lst[1],
                    "port":             lst[2],
                    "player_name":      lst[3],
                    "score":            lst[4],
                    "time_stamp":       time.time(),
                }
            return reply_dictionary  # id, ip, port, nick, score, event type

        if splitted_line[0] == "[server]:":
            if splitted_line[1] == "client":
                result = re.search("\[server\]: client dropped. cid=(\d+)", line)
                ide = list(result.groups())
                ide.append("LEAVE")
                reply_dictionary = \
                    {
                        "event_type":        ide[-1],
                        "player_id":         ide[0],
                        "time_stamp":       time.time(),
                    }
                return reply_dictionary
            if "cid=" in splitted_line[1] or "ClientID=" in splitted_line[1]:
                return {"event_type": "COMMAND", "time_stamp": time.time()}
            if splitted_line[1] == "player":
                return {"event_type": "CONNECTING", "time_stamp": time.time()}
            else:
                return {"event_type": "UNKNOWN", "time_stamp": time.time(), "line": line}
        else:
            return {"event_type": "UNKNOWN", "time_stamp": time.time(), "line": line}
            #b'[Console]: hei\n'

    def conversation(self, line, teamchat):
        """
        ## conversation()
        Conversation is the function that handles chat messages and parses information from them.
        This information includes nick, the message, team id, player id and none which can be used to determine if message went to wrong location.
        if the information is correct "none" is False since we do have info
        if we got wrong "non chat" line we return none with value True, after all we have no info at all.
        """
        print(type(line))
        if (line.split(" ")[0] == "[chat]:" or line.split(" ")[0] == "[teamchat]:") and line.split(" ")[1] != "***":
            if teamchat:
                result = re.search("\[teamchat\]: (\d+):(.+):(.+): (.+)", line)
            else:
                result = re.search("\[chat\]: (\d+):(.+):(.+): (.+)", line)
            name = result.groups()[2]
            ide = result.groups()[0]
            message = result.groups()[-1]
            team_chat = result.groups()[1]
            info = [name, message, ide, team_chat]
            return info
        #[chat]: 0:-2:LeveL 5: mo
        else:
            info = ["NONE", "NONE", "NONE"]
            return info

    def Weaponsolv(self, id):
        id = str(id)
        dic =  {"-1":"hit on a kill tile",
                "-2":"kill command",
                "-3":"changing team/leaving",
                "1": "pistol",
                "0": "hammer",
                "2": "shotgun",
                "3": "grenade",
                "4": "rifle"}
        hit = dic.get(id)
        if hit is not None:
            return hit
        else:
            return "something magical.."

    def Itemsolv(self, id1, id2):
        id1 = int(id1)
        id2 = int(id2)
        if id1 > 1:
            return self.Weaponsolv(id2)
        if id1 == 0:
            return "heart"
        if id1 == 1:
            return "armor"
        else:
            return "something magical.."
