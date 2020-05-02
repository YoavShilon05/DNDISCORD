import discord
from discord.ext import commands
import pickle
from Player import Player
from Character import Character

bot = commands.Bot(command_prefix="d.")
TOKEN = 'NzA2MjE2OTkxMDA1ODY4MDgz.Xq3B8g.49p3sHDPLklsmNmd2A6L5IwG9Uo' \
        ''
players = {}

# FUNCTIONS ____________________________________________________________________________________________________________


async def MakeCharacter(ctx : commands.Context):

    def WaitForMsg(startingMsg, failMsg="Your answer was not valid. try again mate.", condition=lambda m: m):

        if startingMsg != "":
            ctx.send(startingMsg)

        msg = bot.wait_for('message', check=lambda m: m.author == ctx.author)

        if condition(msg):
            return startingMsg
        else:
            ctx.send(failMsg)
            WaitForMsg("", failMsg, condition)


    newCharacter = Character(
        WaitForMsg("What is you character's name?"),



    )




# PLAYERS_______________________________________________________________________________________________________________

# Reset Players ________
import ResetPlayers
# ______________________

try:
    with open("Players.dat", 'r') as f:
        players = pickle.load(f)
except:
    pass

# COMMANDS______________________________________________________________________________________________________________

@bot.event
async def on_ready():
    print("ready")

@bot.command()
async def connect(ctx : commands.Context):

    if ctx.author in players:
        pass
    else:
        await ctx.send("I see you are new here, what nickname would you like to have?")
        nickname = bot.wait_for('message', check=lambda m : m.author == ctx.author)
        players[ctx.author] = Player(ctx.author, nickname)






bot.run(TOKEN)