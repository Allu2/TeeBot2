__author__ = 'Aleksi'
class additional_Plugins():
    def __init__(self, plugin_loader):
        self.register = plugin_loader.register
        from Plugins import API
        self.register(API.API())