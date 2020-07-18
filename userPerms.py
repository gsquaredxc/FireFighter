import discord


# will be more complex later

def has_admin_perms(member):
    return member.guild_permissions.administrator
