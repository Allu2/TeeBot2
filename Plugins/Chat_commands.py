__author__ = 'Aleksi'
class Chat:

    def __init__(self):
        self.handle_events = ["CHAT"]
        self.commands = "commands.cfg"
        pass
    def handle(self, event, bot):
        bot.debug("Chat_Commands is handling this.","PLUGIN")
        msg = event[1]
        nick = event[0]
        id = event[2]
        if "!" == msg.decode()[0]:
            with open(self.commands, "r", encoding="utf-8") as cmds:
                msgg = msg.decode()
                print("We got: {} as mssg.".format(msgg))
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
            bot.say("Largest killing spree: " + str(tee.largest_spree))
            bot.say("Largest multikill: " + str(tee.largest_multikill))
            bot.say("Total kills: " + str(tee.kills))
        if "/pause" == msg.decode():
            bot.say("One does not simply pause an online game!")