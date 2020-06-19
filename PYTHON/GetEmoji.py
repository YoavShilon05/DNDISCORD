
"""this file is meant to make a short program to convert discord emoji to string, no implementations in game."""

from discord.ext import commands

bot = commands.Bot(command_prefix="d.")

TOKEN = 'TOKEN' \
        ''

@bot.event
async def on_reaction_add(reaction, user):
    print(reaction.emoji)


bot.run(TOKEN)