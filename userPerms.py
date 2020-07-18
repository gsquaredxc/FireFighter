import discord
import config


# will be more complex later
from configUtils import get_value


def has_admin_perms(member):
    return member.guild_permissions.administrator


async def has_admin_perms_server(member, guild):
    new_member = await guild.fetch_member(member.id)
    return new_member.guild_permissions.administrator


async def check_if_can_delete(member, guild):
    return get_value(guild,"allow_delete_all") or await has_admin_perms_server(member, guild)


async def check_if_can_ban(member, guild):
    return get_value(guild,"allow_ban_all") or await has_admin_perms_server(member, guild)
