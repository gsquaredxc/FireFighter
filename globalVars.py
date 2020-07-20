import os

import discord

from config import Config

gConfig = Config("guilds.json")
keywordConfig = Config("keywords.json")
userConfig = Config("users.json")

VERSION = discord.__version__

DEBUG = os.getenv("DEBUG") == "1"

new_feature = VERSION != '1.3.4'

gDefaultConf = {
    "baseConfig": {
        "role_spam_base": 3,
        "mute_role": 0,
        "user_age_max": 5,
        "role_spam_mult": 3,
        "allow_delete_all": True,
        "ping_spam_base": 3,
        "ping_spam_mult": 3,
        "user_age_mult": 1,
        "user_age_0": 10,
        "allow_ban_all": False,
        "report_to_spam_channel": 20,
        "mute": 50,
        "spam_channel": 733890159103311933,
        "report_to_all": 25,
        "ping_spam_min": 3,
        "role_spam_min": 3
    }
}

kDefaultConf = {}

userDefaultConf = {}


def init_configs():
    gConfig.open_conf(default_config=gDefaultConf)
    keywordConfig.open_conf(default_config=kDefaultConf)
    userConfig.open_conf(default_config=userDefaultConf)
