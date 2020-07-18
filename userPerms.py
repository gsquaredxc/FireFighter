import discord
import config


# will be more complex later

def has_admin_perms(member):
    return member.guild_permissions.administrator


def has_admin_perms_server(member, guild):
    return guild.fetch_member(member.id).guild_permissions.administrator


def check_if_can_delete(member, guild):
    return config.Config[str(guild.id)]["allow_delete_all"] or has_admin_perms_server(member, guild)


def check_if_can_ban(member, guild):
    return config.Config[str(guild.id)]["allow_ban_all"] or has_admin_perms_server(member, guild)
