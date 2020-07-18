def embedAppender(embed,title,append,appendFail = ""):
    done = False
    for i in range(len(embed.fields)):
        if embed.fields[i].name == title:
            done = True
            embed.set_field_at(i,name=embed.fields[i].name,value=embed.fields[i].value+append,inline=embed.fields[i].inline)
    if not done:
        embed.add_field(name="Actions taken: ", value=appendFail, inline=False)
    return embed
