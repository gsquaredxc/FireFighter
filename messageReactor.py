import globalVars


async def all_reactions(message):
    reactions = []
    if globalVars.gConfig.get_value(message.guild.id,"allow_delete_all"):
        reactions.append('🗑️')
    if globalVars.gConfig.get_value(message.guild.id,"allow_ban_all"):
        reactions.append('🔨')
    for emoji in reactions:
        await message.add_reaction(emoji)


async def spam_reactions(message):
    reactions = ['🗑️', '🔨']
    for emoji in reactions:
        await message.add_reaction(emoji)
