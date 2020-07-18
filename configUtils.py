import config


def get_value(guildID, key):
    try:
        return config.Config[str(guildID)][key]
    except:
        config.Config[str(guildID)][key] = None
        return None


def set_value(guildID, key, value):
    config.Config[str(guildID)][key] = value
