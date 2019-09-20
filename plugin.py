# -*- encoding: utf-8 -*-
# main1.py
import os, zipfile, sys, configparser, io


class Platform:
    def __init__(self):
        self.loadPlugins()

    def sayHello(self, from_):
        print("hello from %s." % from_)

    def loadPlugins(self):
        for filename in os.listdir("plugins"):
            if not filename.endswith(".zip"):
                continue
            self.runPlugin(filename)

    def runPlugin(self, filename):
        pluginPath = os.path.join("plugins", filename)
        print(pluginPath)
        pluginInfo, plugin = self.getPlugin(pluginPath)
        print("loading plugin: %s, description: %s" %
              (pluginInfo["name"], pluginInfo["description"]))
        plugin.setPlatform(self)
        plugin.start()

    def getPlugin(self, pluginPath):
        pluginzip = zipfile.ZipFile(pluginPath, "r")
        # print(pluginzip.namelist())
        description_txt = io.TextIOWrapper(pluginzip.open("description.txt"))
        # print(description_txt.read())
        parser = configparser.ConfigParser()
        parser.read_string(description_txt.read())
        print(parser.sections())
        pluginInfo = {}
        pluginInfo["name"] = parser.get("general", "name")
        pluginInfo["description"] = parser.get("general", "description")
        pluginInfo["code"] = parser.get("general", "code")

        sys.path.append(pluginPath)
        moduleName, pluginClassName = pluginInfo["code"].rsplit(".", 1)
        module = __import__(moduleName, fromlist=[pluginClassName, ])
        pluginClass = getattr(module, pluginClassName)
        plugin = pluginClass()
        return pluginInfo, plugin


if __name__ == "__main__":
    platform = Platform()

