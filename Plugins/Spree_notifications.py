__author__ = 'Aleksi'
import threading
class Spree:
    def __init__(self):
        self.handle_events = ["KILL"]
        pass
    def handle(self, event, bot):
        print("Spree_notifications is handling this.")
        if event[-1] == "KILL" and event[-3] != b'-3':
            # bot.debug("We got event: {}".format(event), "DEBUG")
            try:
                killer_tee = bot.get_Tee(event[0])
            except (KeyError, NameError) as e:
                bot.debug("Tee didn't exist! Updating player list!", "DEBUG")
                bot.writeLine("status")
            killer_tee.set_spree(killer_tee.get_spree() + 1)
            if killer_tee.get_idnum() == event[2]: #In case of suicide
                killer_tee.set_spree(0)
                killer_tee.multikill = 0

            else:
                victim_tee = bot.get_Tee(event[2])
                if victim_tee.get_spree() >= 5:
                    t = threading.Timer(5, bot.shutdown, args=[victim_tee, killer_tee, victim_tee.get_spree()])
                    t.start()

                victim_tee.set_spree(0)
                bot.Multikill(event[0])
                bot.killSpree(event[0])
        pass