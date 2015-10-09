__author__ = 'Aleksi'
from subprocess import check_output
class Stats:
    def __init__(self):
        self.handle_events = ["NOTHING"]
        pass
    def handle(self, event, bot, plugins):
        bot.debug("Statistics is handling this.")
        msg = event[1]
        nick = event[0]
        id = event[2]
        if "/stats" == msg.decode():
            tee = bot.get_Tee(id)
            bot.say("Player: " + tee.get_nick().decode('utf-8'))
            bot.say("Largest killing spree: " + str(tee.get_largest_spree()))
            bot.say("Largest multikill: " + str(tee.get_largest_multikill()))
            bot.say("Total kills: " + str(tee.attributes["kills"]))
        if "/pause" == msg.decode() or "/stop" == msg.decode():
            bot.say("One does not simply pause an online game!")
        if "/lag" == msg.decode():
            lag = str(check_output(["ifstat", "1", "1"])).split()
            down = lag[-2]
            up = lag[-1].replace("\\", "").replace("n", "").replace("\n","").replace("'", "")
            bot.say("In: {}kb/s  Out: {}kb/s.".format(down, up))