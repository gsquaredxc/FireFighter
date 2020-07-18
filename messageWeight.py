import datetime
import os

from configUtils import get_value

DEBUG = os.getenv("DEBUG") == "1"

import config


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
    # time_since_join_weight(message)
    if DEBUG:
        print("USER_AGE_WEIGHT: " + str(user_age))
    return user_age


def ping_counter(message) -> int:
    mentions = len(message.mentions)
    role_mentions = len(message.role_mentions)
    if mentions >= get_value(message.guild.id,"ping_spam_min"):
        if DEBUG:
            print("PATH: PING_SPAM; MENTIONS: " + str(mentions))
        return get_value(message.guild.id,"ping_spam_base") + (get_value(message.guild.id,"ping_spam_mult") * mentions)
    if role_mentions >= get_value(message.guild.id,"role_spam_min"):
        if DEBUG:
            print("PATH: ROLE_SPAM; MENTIONS: " + str(role_mentions))
        return get_value(message.guild.id,"role_spam_base") + (get_value(message.guild.id,"role_spam_mult") * role_mentions)
    return 0


def user_age_weight(message) -> int:
    now = datetime.datetime.now()
    difference = (now - message.author.created_at).days
    if DEBUG:
        print("USER_AGE: " + str(difference))
    if difference == 0:
        return get_value(message.guild.id,"user_age_0")
    elif difference < get_value(message.guild.id,"user_age_max"):
        return get_value(message.guild.id,"user_age_mult") * (
                get_value(message.guild.id,"user_age_max") - difference)
    return 0
