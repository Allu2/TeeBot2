__author__ = 'Aleksi'
import threading, default_Plugins, additional_Plugins #rename additional_Plugins and add loading of custom plugins there.
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
            if event["event_type"] in x.handle_events or "*" in x.handle_events:
                t = threading.Thread(target=x.handle, args=(event, self.teeBot, self.plugins))
                thread_list.append(t)
                t.start()
        for x in thread_list:
            #x.start
            x.join()

    def initialize(self):
        default = default_Plugins.default_Plugins(self)
        additional = additional_Plugins.additional_Plugins(self)

