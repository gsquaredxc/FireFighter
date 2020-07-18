import os
import re

import discord
from dotenv import load_dotenv

from discord.ext import commands

import config as conf
from messageReactor import all_reactions
from messageWeight import message_weigher
from userPerms import has_admin_perms

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

print("Loading config")
conf.open_conf()

bot = commands.Bot(command_prefix="%")


@bot.command()
async def config(ctx, arg1, arg2):
    if has_admin_perms(ctx.author):
        try:
            conf.Config[str(ctx.guild.id)][arg1] = int(arg2)
        except ValueError:
            conf.Config[str(ctx.guild.id)][arg1] = arg2

@bot.command()
async def save_conf(ctx):
    if has_admin_perms(ctx.author):
        print("Saving config")
        conf.open_conf()

@bot.command()
async def load_conf(ctx):
    if has_admin_perms(ctx.author):
        print("Loading config")
        conf.save_conf()

@bot.command()
async def init(ctx):
    if has_admin_perms(ctx.author):
        conf.Config[str(ctx.guild.id)] = conf.Config["baseConfig"]


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    global global_channel
    global_channel = bot.get_channel(conf.Config["baseConfig"]["spam_channel"])

@bot.event
async def on_message(message):
    if message.author == bot.user:
        pass
    elif message.content == "%init":
        if has_admin_perms(message.author):
            conf.Config[str(message.guild.id)] = conf.Config["baseConfig"]
    else:
        weight = message_weigher(message)
        i = 0
        if weight >= conf.Config[str(message.guild.id)]["report_to_all"] or weight >= \
                conf.Config[str(message.guild.id)]["report_to_spam_channel"]:
            embedVar = discord.Embed(title="Suspicious message", color=0x00ff00)
            embedVar.add_field(name="Message content:", value=message.content, inline=False)
            embedVar.add_field(name="Message weight:", value=str(weight), inline=False)
            embedVar.add_field(name="Author:", value=message.author.mention, inline=True)
            embedVar.add_field(name="Full name:", value=str(message.author), inline=True)
            embedVar.add_field(name="ID:", value=message.author.id, inline=False)
            embedVar.add_field(name="Author age:", value=message.author.created_at, inline=True)
            embedVar.add_field(name="Message ID:", value = message.id, inline=False)
            embedVar.add_field(name="Channel:", value=message.channel.mention, inline=False)
        if weight >= conf.Config[str(message.guild.id)]["report_to_all"]:
            message = await global_channel.send(embed=embedVar)
            await all_reactions(message)
        if weight >= conf.Config[str(message.guild.id)]["report_to_spam_channel"]:
            message = await bot.get_channel(int(conf.Config[str(message.guild.id)]["spam_channel"])).send(embed=embedVar)
            await all_reactions(message)
        if weight >= conf.Config[str(message.guild.id)]["mute"]:
            pass  # TODO
    await bot.process_commands(message)
    return

@bot.event
async def on_reaction_add(reaction,user):
    if reaction.message.author == bot.user:
        if reaction.emoji == '🗑️':
            if has_admin_perms(user):
                for field in reaction.message.embeds[0].to_dict()["fields"]:
                    if field["name"] == "Message ID:":
                        messageID = int(field["value"])
                    elif field["name"] == "Channel:":
                        channelID = int(re.sub('[^0-9]','', field["value"]))
                message = await bot.get_channel(channelID).fetch_message(messageID)
                await message.delete()



try:
    bot.run(TOKEN)
except KeyboardInterrupt as e:  # Catches keyboard interrupt
    print(e)
finally:
    print("Saving config")
    conf.save_conf()
