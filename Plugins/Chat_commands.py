__author__ = 'Aleksi'
from subprocess import check_output
class Chat:

    def __init__(self):
        self.handle_events = ["CHAT"]
        self.commands = "commands.cfg"
        pass
    def handle(self, event, bot, plugins):
        bot.debug("Chat_Commands is handling this.")
        msg = event["message"]
        nick = event["player_name"]
        id = event["player_id"]
        if "!" == msg.decode()[0]:
            with open(self.commands, "r", encoding="utf-8") as cmds:
                msgg = msg.decode()
                print("We got: {} as msgg.".format(msgg))
                lines = cmds.readlines()
                for x in lines:
                    split = x.split(" _ ")
                    if split[0] == msgg:
                        print(x)
                        bot.say(split[1].rstrip("\n"))
                    else:
                        pass
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
