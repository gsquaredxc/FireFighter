import os
import re
import sys

import discord
from dotenv import load_dotenv

from discord.ext import commands

import config as conf
from embedUtils import embedAppender
from messageReactor import all_reactions, spam_reactions
from messageWeight import message_weigher
from userPerms import has_admin_perms, check_if_can_ban, check_if_can_delete

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEBUG = os.getenv("DEBUG") == "1"

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

@bot.command()
async def restart(ctx):
    if ctx.guild.id == 733383903544606800:
        if has_admin_perms(ctx.author):
            sys.exit()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Activity()
    game.name = "for spammers"
    game.type = discord.ActivityType.watching
    await bot.change_presence(status=discord.Status.online, activity=game)
    global global_channel
    global_channel = bot.get_channel(conf.Config["baseConfig"]["spam_channel"])


@bot.event
async def on_message(message):
    if message.author == bot.user:
        pass
    else:
        weight = message_weigher(message)
        if weight >= conf.Config[str(message.guild.id)]["report_to_all"] or weight >= \
                conf.Config[str(message.guild.id)]["report_to_spam_channel"]:
            embedVar = discord.Embed(title="Suspicious message", color=0x00ff00)
            embedVar.add_field(name="Message content:", value=message.content, inline=False)
            embedVar.add_field(name="Message weight:", value=str(weight), inline=False)
            embedVar.add_field(name="Author:", value=message.author.mention, inline=True)
            embedVar.add_field(name="Full name:", value=str(message.author), inline=True)
            embedVar.add_field(name="ID:", value=message.author.id, inline=False)
            embedVar.add_field(name="Author age:", value=message.author.created_at, inline=True)
            embedVar.add_field(name="Message ID:", value=message.id, inline=False)
            embedVar.add_field(name="Channel:", value=message.channel.mention, inline=False)
        if weight >= conf.Config[str(message.guild.id)]["mute"]:
            embedVar.add_field(name="Actions taken:", value="Muted", inline=False)
            role = message.guild.get_role(conf.Config[str(message.guild.id)]["mute_role"])
            await message.author.add_roles(role)
        if weight >= conf.Config[str(message.guild.id)]["report_to_all"]:
            send_message = await global_channel.send(embed=embedVar)
            await all_reactions(send_message)
        if weight >= conf.Config[str(message.guild.id)]["report_to_spam_channel"]:
            send_message = await bot.get_channel(int(conf.Config[str(message.guild.id)]["spam_channel"])).send(
                embed=embedVar)
            await spam_reactions(send_message)
    await bot.process_commands(message)
    return


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == bot.user:
        if has_admin_perms(user):
            if reaction.emoji == '🗑️':
                for field in reaction.message.embeds[0].to_dict()["fields"]:
                    if field["name"] == "Message ID:":
                        messageID = int(field["value"])
                    elif field["name"] == "Channel:":
                        channelID = int(re.sub('[^0-9]', '', field["value"]))
                channel = bot.get_channel(channelID)
                message = await channel.fetch_message(messageID)
                if await check_if_can_delete(user, channel.guild):
                    await message.delete()
                    await reaction.message.edit(embed = embedAppender(reaction.message.embeds[0],"Actions taken:", ", message deleted","Message deleted"))
            elif reaction.emoji == '🔨':
                for field in reaction.message.embeds[0].to_dict()["fields"]:
                    if field["name"] == "ID:":
                        memberID = int(field["value"])
                    elif field["name"] == "Channel:":
                        channelID = int(re.sub('[^0-9]', '', field["value"]))
                channel = bot.get_channel(channelID)
                member = await channel.guild.fetch_member(memberID)
                if await check_if_can_ban(user, channel.guild):
                    await member.ban(reason="Caught spamming by FireFighter")
                    await reaction.message.edit(embed = embedAppender(reaction.message.embeds[0],"Actions taken:", ", banned","Banned"))


try:
    bot.run(TOKEN)
except KeyboardInterrupt as e:  # Catches keyboard interrupt
    print(e)
finally:
    print("Saving config")
    conf.save_conf()
