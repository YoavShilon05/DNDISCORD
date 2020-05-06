import discord
from discord.ext import commands
import pickle
import asyncio
from typing import *
import GlobalVars
from copy import copy

from Player import Player
from Character import Character
from Races import Races
from Professions import Professions
from Menu import Menu

bot = commands.Bot(command_prefix="d.")
GlobalVars.bot = bot

TOKEN = 'NzA2MjE2OTkxMDA1ODY4MDgz.XrLYFg.VH2-yjc2EPx_Nv9QmFCFuz_9P5o' \
        ''
onlinePlayers : Dict[discord.Member, Player] = {}

# FUNCTIONS ____________________________________________________________________________________________________________


async def MakeCharacter(ctx : commands.Context):

    async def WaitForMsg(startingMsg, failMsg="Your answer is not valid.", condition=lambda m: True):

        if startingMsg != "":
            await ctx.send(startingMsg)

        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)

        if condition(msg):
            return startingMsg
        else:
            await ctx.send(failMsg)
            await WaitForMsg("", failMsg, condition)

    racesStr = ""
    for r in Races:
        # if race is good / hero race:
        if r.value[0] == 0:
            racesStr += r.name + "\n"

    professionsStr = '\n'.join([p.name for p in Professions])

    newCharacter = Character(
        await WaitForMsg("What is your character's name?"),
        # if the sexes ever change, change that although idk why would they change i mean what?
        await WaitForMsg("What is your character's sex?\npossible sexes are -\nmale\nfemale\nunknown", condition=lambda m : m.content.lower() in ['male', 'female', 'unknown']),
        await WaitForMsg("What will your character's race be?\nPossible races are:\n" + racesStr, "Couldn't find that race.", lambda m: m.content.lower() in [r.name.lower() for r in Races]),
        await WaitForMsg("What will your character's profession be?\nPossible professions are:\n" + professionsStr, "Couldn't find that profession.", lambda m: m.content.lower() in [p.name.lower() for p in Professions]),
        await WaitForMsg("What is your character's backstory?")

    )

    return newCharacter

def UpdatePlayers():
    with open("Players.dat", 'wb') as f:

        pickledPlayers = {}

        for author, player in players.items():
            pickledPlayer = copy(player)
            pickledPlayer.author = None
            pickledPlayers[author.id] = pickledPlayer

        pickle.dump(pickledPlayers, f)

def GetPlayers():

    with open('Players.dat', 'rb') as f:
        pickledPlayers = pickle.load(f)

        newPlayers = {}
        for id, player in pickledPlayers.items():
            player.author = bot.get_user(id)
            newPlayers[bot.get_user(id)] = player
        return newPlayers



# COMMANDS______________________________________________________________________________________________________________
players: Dict[discord.Member, Player]
@bot.event
async def on_ready():
    print("ready")

    # PLAYERS_______________________________________________________________________________________________________________

    global players
    players = GetPlayers()

@bot.command()
async def connect(ctx : commands.Context):

    if ctx.author in players:
        await ctx.send(f"Welcome back {players[ctx.author].nickname}!")
    else:
        await ctx.send("I see you are new here, what nickname would you like to have?")
        nickname = await bot.wait_for('message', check=lambda m : m.author == ctx.author)
        newPlayer = Player(ctx.author, nickname.content)
        players[ctx.author] = newPlayer
        UpdatePlayers()


        #TODO: un-comment dat:

        #await ctx.send(f"Hello {nickname.content}! Lets make your first character.")
        #await asyncio.sleep(2)
        #character = await MakeCharacter(ctx)

        #newPlayer.AddCharacter(character)


@bot.command()
async def get_players(ctx : commands.Context):
    if len(players) > 0:
        playerNames = []
        for author, player in players.items():
            playerNames.append(author.name + " : " + player.nickname)

        await ctx.send(',\n'.join(playerNames))
    else:
        await ctx.send("no players were found.")

mainMenu = Menu("This is a menu.", "🍆", [])


#🌍
#🦾
#🖐️
#➡️
#🛠️
@bot.command()
async def test_menu(ctx : commands.Context):
    await mainMenu.Send(ctx.channel, players[ctx.author])

reactions = []
@bot.event
async def on_reaction_add(reaction, user):
    reactions.append(reaction)


bot.run(TOKEN)