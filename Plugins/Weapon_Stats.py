__author__ = 'Aleksi'

class Weapon_Stats:

    def __init__(self):
        self.handle_events = ["CHAT","KILL", "PICKUP"]
        self.weapons = ["shotgun", "rifle", "pistol", "hammer", "grenade"]
        pass
    def handle(self, event, bot, plugins):
        bot.debug("Weapon Stats is handling this.")
        bot.logger.debug("We got event: {}".format(event))
        if event["event_type"] == "KILL":
            weapon = bot.events.Weaponsolv(int(event["user_weapon_id"]))
            bot.debug("We got weapon: {}".format(weapon))
            id = int(event["killer_id"])
            try:
                tee = bot.get_Tee(id)
                try:
                    if weapon in self.weapons:
                        tee.attributes[weapon+"_kills"] = tee.attributes[weapon+"_kills"]+1
                except Exception as e:
                    bot.debug("We got weapon {}".format(weapon))
                    bot.exception(e)
                    tee.attributes[weapon+"_kills"] = 1
            except Exception as e:
                bot.exception(e)
                return 0
        if event["event_type"] == "PICKUP":
            id = event["player_id"]
            try:
                tee = bot.get_Tee(id)
                try:
                    if event["name"] in self.weapons:
                        tee.attributes[event["name"]+"_picks"] = tee.attributes[event["name"]+"_picks"]+1
                except Exception as e:
                    tee.attributes[event["name"]+"_picks"] = 1
            except Exception as e:
                bot.exception(e)
                return 0
        if event["event_type"] == "CHAT":
            msg = event["message"]
            tee = bot.get_Tee(event["player_id"])
            for wep in self.weapons:
                if "/"+wep == msg and tee.get_nick() == "blackdevil" :
                    nick = tee.get_nick()
                    bot.say("Our angel with a shotgun")
                    try:
                        bot.say("Has picked up {} {} times".format(wep, tee.attributes[wep+"_picks"]))
                    except Exception as e:
                        pass
                    try:
                        bot.say("and killed with it {} times".format(tee.attributes[wep+"_kills"]))
                    except Exception as e:
                        pass

                elif "/"+wep == msg and tee.get_nick() != "blackdevil":
                    nick = tee.get_nick()
                    bot.say("Player: {} {} stats:".format(nick, wep))
                    try:
                        bot.say("Has picked up {} {} times".format(wep, tee.attributes[wep+"_picks"]))
                    except Exception as e:
                        pass
                    try:
                        bot.say("and killed with it {} times".format(tee.attributes[wep+"_kills"]))
                    except Exception as e:
                        pass

