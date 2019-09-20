# plugins2.py
class Plugin2:
    def setPlatform(self, platform):
        self.platform = platform

    def start(self):
        self.platform.sayHello("plugin2")

