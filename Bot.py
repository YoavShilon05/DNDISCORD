#EXTERNAL LIBRARIES ______________________________________
import GlobalVars
import discord
from discord.ext import commands
import pickle
from typing import *
from copy import copy
import asyncio

# GLOBAL VARS ___________________________________________
bot = commands.Bot(command_prefix="d.")
GlobalVars.bot = bot

# FILES _________________________________________________
from Player import Player, Party
from Character import Character, Races, Professions

from Menu import Menu, Starter
from Adventure import Adventure

TOKEN = 'NzA2MjE2OTkxMDA1ODY4MDgz.XrLYFg.VH2-yjc2EPx_Nv9QmFCFuz_9P5o' \
        ''

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
    with open("./Players.dat", 'wb') as f:

        pickledPlayers = {}

        for authorId, player in players.items():
            pickledPlayer = copy(player)
            pickledPlayer.author = None
            pickledPlayer.Reset()
            pickledPlayers[authorId] = pickledPlayer

        pickle.dump(pickledPlayers, f)

def LoadPlayers():

    with open('./Players.dat', 'rb') as f:
        pickledPlayers = pickle.load(f)

        newPlayers = {}
        for id, player in pickledPlayers.items():
            player.author = bot.get_user(id)
            player.party = Party([player])
            newPlayers[id] = player
        return newPlayers

def LoadAdventures():

    with open('Adventures.dat', 'rb') as f:
        adventures = pickle.load(f)

# COMMANDS______________________________________________________________________________________________________________
players: Dict[int, Player] = {}
adventures : List[Adventure]
@bot.event
async def on_ready():
    print("ready")

    # PLAYERS_____________________________________________________________________________________________________________
    global players
    players = LoadPlayers()
    GlobalVars.players = players



@bot.command()
async def get_players(ctx : commands.Context):
    if len(players) > 0:
        playerNames = []
        for author, player in players.items():
            playerNames.append(author.name + " : " + player.nickname)

        await ctx.send(',\n'.join(playerNames))
    else:
        await ctx.send("no players were found.")

async def StartAdventure(channel, party, adventure : Adventure):
    await adventure.Init(channel, party)

    Playing = True
    while Playing:

        msg : discord.Message = await bot.wait_for('message', check= lambda m : players[m.author] == adventure.turn)
        result = await adventure.ExecuteCommand(msg, players[msg.author])

async def CommunityAdventures(channel : discord.TextChannel, player : Player):

    adventuresPlayed = []
    party = player.party

    for p in party:
        adventuresPlayed.extend(p.adventuresPlayed)

    for a in adventures:
        if a not in adventuresPlayed:
            await StartAdventure(channel, party, a)

communityAdventures = Starter("Community Adventures", "🖐️", CommunityAdventures)
computerAdventures = Starter("Computer Generated Adventure", "🦾", CommunityAdventures)
async def Pass():
    pass
adventureBuilder = Starter("Adventure Builder", "🛠️", Pass)

quickPlay = Menu("Quick Play", "➡️", [communityAdventures, computerAdventures])
campaign = Menu("Campaign", "🌍", [])
mainMenu = Menu("Main Menu", "🍆", [campaign, quickPlay, adventureBuilder])


#🌍
#🦾
#🖐️
#➡️
#🛠️

declineInvite = '⛔'
acceptInvite = '✅'

@bot.command()
async def start(ctx : commands.Context):
    if ctx.author.id in players.keys():
        await ctx.send(f"Welcome back {players[ctx.author.id].nickname}!")
    else:
        await ctx.send(f"Welcome to the crew {ctx.author.name}")
        newPlayer = Player(ctx.author)
        players[ctx.author.id] = newPlayer
        GlobalVars.players[ctx.author.id] = newPlayer
        UpdatePlayers()

        await asyncio.sleep(2)

        await ctx.send(f"Lets make your first character.")

        await asyncio.sleep(1.25)

        character = await MakeCharacter(ctx)
        newPlayer.AddCharacter(character)

    await mainMenu.Send(ctx.channel, players[ctx.author.id])



# PARTY COMMANDS _______________________________________________________________________________________________________

@bot.command(aliases=['invite'])
async def inv(ctx : commands.Context, member : discord.Member):

    invitationTimeout = 300

    sender = players[ctx.author.id]

    invitation = await member.send(f"{ctx.author.mention} has invited you to a party", delete_after=invitationTimeout)
    await invitation.add_reaction(acceptInvite)
    await invitation.add_reaction(declineInvite)

    await ctx.send(f"Invited {member.mention} to the party.")

    reaction, user = await bot.wait_for('reaction_add', check=lambda r, u : r.emoji == acceptInvite or r.emoji == declineInvite, timeout=invitationTimeout)

    try:
        await invitation.delete()
    except commands.CommandInvokeError:
        await ctx.send(f"the invitation for {user.mention} has expired")

    receiver = players[user.id]

    if reaction.emoji == acceptInvite:
        sender.party.AddPlayer(receiver)
        await ctx.send(f"{user.mention} has joined your party!")
    else:
        await ctx.send(f"{user.mention} has declined your party invitation")


@bot.command(aliases=['p'])
async def party(ctx):
    player = players[ctx.author.id]
    ctx.send(", ".join([p.author.mention for p in player.party]))

bot.run(TOKEN)