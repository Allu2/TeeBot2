__author__ = 'Aleksi'
import threading
class Plugin_loader:
    def __init__(self, bot):
        self.teeBot = bot
        self.plugins = []
        self.initialize()
    def register(self, plugin):
        self.plugins.append(plugin)
        pass
    def event_handler(self, event):
        thread_list = []
        for x in self.plugins:
            if event[-1] in x.handle_events or "*" in x.handle_events:
                t = threading.Thread(target=x.handle, args=(event, self.teeBot,))
                thread_list.append(t)
                t.start()
        for x in thread_list:
            #x.start
            x.join()

    def initialize(self):
        from Plugins import Chat_commands
        self.register(Chat_commands.Chat())
        from Plugins import Spree_notifications
        self.register(Spree_notifications.Spree())
        from Plugins import Statistics
        self.register(Statistics.Stats())
        from Plugins import Chat_Logger
        self.register(Chat_Logger.Logger())
        from Plugins import Whois
        self.register(Whois.Whois())
        from Plugins import ChatBot
        self.register(ChatBot.ChatBot())
        from Plugins import Domination
        self.register(Domination.Domination())
        from Plugins import Essentials
        self.register(Essentials.Essentials())
        from Plugins import Blacky_Shotgun
        self.register(Blacky_Shotgun.Blacky_Shotgun())
