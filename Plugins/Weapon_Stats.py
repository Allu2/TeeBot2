__author__ = 'Aleksi'

class Weapon_Stats:

    def __init__(self):
        self.handle_events = ["CHAT","KILL", "PICKUP"]
        self.weapons = ["shotgun", "rifle", "pistol", "hammer", "grenade"]
        pass
    def handle(self, event, bot, plugins):
        bot.debug("Weapon Stats is handling this.")
        bot.logger.debug("We got event: {}".format(event))
        if event[-1] == "KILL":
            weapon = bot.events.Weaponsolv(int(event[4].decode()))
            bot.debug("We got weapon: {}".format(weapon))
            id = int(event[0])
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
        if event[-1] == "PICKUP":
            id = event[0]
            try:
                tee = bot.get_Tee(id)
                try:
                    if event[-2] in self.weapons:
                        tee.attributes[event[-2]+"_picks"] = tee.attributes[event[-2]+"_picks"]+1
                except Exception as e:
                    tee.attributes[event[-2]+"_picks"] = 1
            except Exception as e:
                bot.exception(e)
                return 0
        if event[-1] == "CHAT":
            msg = event[1]
            tee = bot.get_Tee(event[2])
            for wep in self.weapons:
                if "/"+wep == msg.decode() and tee.get_nick().decode() == "blackdevil" :
                    nick = tee.get_nick().decode()
                    bot.say("Our angel with a shotgun")
                    try:
                        bot.say("Has picked up {} {} times".format(wep, tee.attributes[wep+"_picks"]))
                    except Exception as e:
                        pass
                    try:
                        bot.say("and killed with it {} times".format(tee.attributes[wep+"_kills"]))
                    except Exception as e:
                        pass

                elif "/"+wep == msg.decode() and tee.get_nick().decode() != "blackdevil":
                    nick = tee.get_nick().decode()
                    bot.say("Player: {} {} stats:".format(nick, wep))
                    try:
                        bot.say("Has picked up {} {} times".format(wep, tee.attributes[wep+"_picks"]))
                    except Exception as e:
                        pass
                    try:
                        bot.say("and killed with it {} times".format(tee.attributes[wep+"_kills"]))
                    except Exception as e:
                        pass

