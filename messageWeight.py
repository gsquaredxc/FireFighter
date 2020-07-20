import datetime
import os

import globalVars

DEBUG = os.getenv("DEBUG") == "1"


def message_weigher(message) -> int:
    message_w = message_weight(message)
    user_w = user_weight(message)
    if DEBUG:
        print("MESSAGE_WEIGHT: " + str(message_w))
        print("USER_WEIGHT: " + str(user_w))
    return message_w + user_w


def message_weight(message) -> int:
    # messageWeight += keyword_finder(message)
    ping_weight = ping_counter(message)
    return ping_weight


def user_weight(message) -> int:
    user_age = user_age_weight(message)
    user_link = 0
    if globalVars.new_feature:
        user_link = user_link_weight(message)
    time_weight = time_since_join_weight(message)
    if DEBUG:
        print("USER_AGE_WEIGHT: " + str(user_age))
        print("USER_TIME_WEIGHT: " + str(time_weight))
    return user_age - user_link + time_weight


def ping_counter(message) -> int:
    mentions = len(message.mentions)
    role_mentions = len(message.role_mentions)
    return_val = 0
    if mentions >= globalVars.gConfig.get_value(message.guild.id, "ping_spam_min"):
        if DEBUG:
            print("PATH: PING_SPAM; MENTIONS: " + str(mentions))
        return_val += globalVars.gConfig.get_value(message.guild.id, "ping_spam_base") + (
                    globalVars.gConfig.get_value(message.guild.id, "ping_spam_mult") * mentions)
    if role_mentions >= globalVars.gConfig.get_value(message.guild.id, "role_spam_min"):
        if DEBUG:
            print("PATH: ROLE_SPAM; MENTIONS: " + str(role_mentions))
        return_val += globalVars.gConfig.get_value(message.guild.id, "role_spam_base") + (
                    globalVars.gConfig.get_value(message.guild.id, "role_spam_mult") * role_mentions)
    return return_val


def user_age_weight(message) -> int:
    now = datetime.datetime.now()
    difference = (now - message.author.created_at).days
    if DEBUG:
        print("USER_AGE: " + str(difference))
    if difference == 0:
        return globalVars.gConfig.get_value(message.guild.id, "user_age_0")
    elif difference < globalVars.gConfig.get_value(message.guild.id, "user_age_max"):
        return globalVars.gConfig.get_value(message.guild.id, "user_age_mult") * (
                globalVars.gConfig.get_value(message.guild.id, "user_age_max") - difference)
    return 0


def user_link_weight(message) -> int:
    author = message.author
    flags = author.public_flags
    weight = 0
    weight += globalVars.gConfig.get_value(message.guild.id, "user_hypesquad") * flags.hypesquad
    weight += globalVars.gConfig.get_value(message.guild.id, "user_accounts") * len(flags.accounts)
    weight += globalVars.gConfig.get_value(message.guild.id, "user_nitro") * flags.nitro
    return weight


def time_since_join_weight(message) -> int:
    now = datetime.datetime.now()
    difference = (now - message.author.joined_at).days
    if DEBUG:
        print("TIME_JOIN: " + str(difference))
    if difference == 0:
        return globalVars.gConfig.get_value(message.guild.id, "user_join_0")
    elif difference < globalVars.gConfig.get_value(message.guild.id, "user_join_max"):
        return globalVars.gConfig.get_value(message.guild.id, "user_join_mult") * (
                globalVars.gConfig.get_value(message.guild.id, "user_join_max") - difference)
    return 0
