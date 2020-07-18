import os

import discord
from dotenv import load_dotenv

from config import open_conf, save_conf, Config
from messageWeight import message_weigher
from userPerms import has_admin_perms

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

open_conf()

bot = discord.Client()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    global global_channel
    global_channel = bot.get_channel(733897610716381256)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content == "%spam_channel":
        if has_admin_perms(message.author):
            Config[str(message.guild.id)]["spam_channel"] = message.channel.id
        return
    elif message.content == "%init":
        if has_admin_perms(message.author):
            Config[str(message.guild.id)] = Config["baseConfig"]
        return
    else:
        weight = message_weigher(message)
        if weight >= Config[str(message.guild.id)]["report_to_all"] or weight >= Config[str(message.guild.id)]["report_to_spam_channel"]:
            embedVar = discord.Embed(title="Suspicious message", color=0x00ff00)
            embedVar.add_field(name="Message content:", value=message.content, inline=False)
            embedVar.add_field(name="Message weight:", value=str(weight), inline=False)
            embedVar.add_field(name="Author:", value=message.author.mention, inline=True)
            embedVar.add_field(name="Full name:", value=str(message.author), inline=True)
            embedVar.add_field(name="ID:", value=message.author.id, inline=False)
            embedVar.add_field(name="Author age:", value=message.author.created_at, inline=True)
        if weight >= Config[str(message.guild.id)]["report_to_all"]:
            await global_channel.send(embed=embedVar)
        if weight >= Config[str(message.guild.id)]["report_to_spam_channel"]:
            await bot.get_channel(int(Config[str(message.guild.id)]["spam_channel"])).send(embed=embedVar)
        if weight >= Config[str(message.guild.id)]["mute"]:
            pass #TODO
        return


try:
    bot.run(TOKEN)
except BaseException as e:  # Catches keyboard interrupt
    print(e)
finally:
    save_conf()
