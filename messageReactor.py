
async def all_reactions(message):
    reactions = ['🗑️','🔨']
    for emoji in reactions:
        await message.add_reaction(emoji)
