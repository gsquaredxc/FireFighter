import json


class Config:

    def __init__(self, filename):
        self.filename = filename
        self.conf = {}

    def open_conf(self, retry=True, default_config=None):
        self.defaultConf = default_config
        try:
            with open(self.filename) as f:
                self.conf = json.load(f)
        except Exception as e:  # should change this
            print(e)
            if retry:
                with open(self.filename, "a+") as a:
                    json.dump(default_config, a, indent=4)
                self.open_conf(False)

    def save_conf(self):
        with open(self.filename, "w") as f:
            json.dump(self.conf, f, indent=4)

    def get_value(self, guildID, key, defaultConf="baseConfig"):
        try:
            return self.conf[str(guildID)][key]
        except:
            try:
                self.conf[str(guildID)][key] = self.conf[defaultConf][key]
            except:
                self.conf[defaultConf][key] = self.defaultConf[defaultConf][key]
            finally:
                return self.conf[defaultConf][key]

    def set_value(self, guildID, key, value):
        self.conf[str(guildID)][key] = value
