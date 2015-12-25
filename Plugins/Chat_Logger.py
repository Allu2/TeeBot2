__author__ = 'Aleksi'
import time
class Logger:
    def __init__(self):
        self.handle_events = ["CHAT"]
        self.chatlog = "chat.log"
        pass
    def handle(self, event, bot, plugins):
        bot.debug("Chat_Logger is handling this.")
        msg = event["message"]
        nick = event["player_name"]
        with open(self.chatlog, "a", encoding="utf-8") as chatlogi:
            time1 = time.strftime("%c", time.localtime())
            chatlogi.write("[{}] ".format(time1) + "[{0}] ".format(nick) + msg + "\n")