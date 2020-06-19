from discord.ext import commands

bot = commands.Bot(command_prefix="d.")

TOKEN = 'TOKEN' \
        ''

@bot.event
async def on_reaction_add(reaction, user):
    print(reaction.emoji)


bot.run(TOKEN)