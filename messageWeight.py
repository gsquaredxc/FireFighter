import discord

import config


def message_weigher(message) -> int:
    weight = 0
    weight += message_weight(message)
    weight += user_weight(message)
    return weight


def message_weight(message) -> int:
    messageWeight = 0
    # messageWeight += keyword_finder(message)
    messageWeight += ping_counter(message)
    return messageWeight


def user_weight(message) -> int:
    weight = 0
    # weight += user_age_weight(message)
    # weight += time_since_join_weight(message)
    return weight


def ping_counter(message) -> int:
    weight = 0
    mentions = len(message.mentions)
    role_mentions = len(message.role_mentions)
    if mentions >= config.Config[str(message.guild.id)]["ping_spam_min"]:
        weight += config.Config[str(message.guild.id)]["ping_spam_base"] + config.Config[str(message.guild.id)][
            "ping_spam_mult"] * mentions
    if role_mentions >= config.Config[str(message.guild.id)]["role_spam_min"]:
        weight += config.Config[str(message.guild.id)]["role_spam_base"] + config.Config[str(message.guild.id)][
            "role_spam_mult"] * role_mentions
    return weight
