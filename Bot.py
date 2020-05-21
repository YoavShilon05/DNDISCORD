#EXTERNAL LIBRARIES ______________________________________
import GlobalVars
import discord
from discord.ext import commands
import dill
from typing import *
import copy
import asyncio

# GLOBAL VARS ___________________________________________
bot = commands.Bot(command_prefix="d.")
GlobalVars.bot = bot

# FILES _________________________________________________
import Player
import Character
import Menu
import Adventure
from TEST import AddCurency

TOKEN = 'NzA2MjE2OTkxMDA1ODY4MDgz.XrLYFg.VH2-yjc2EPx_Nv9QmFCFuz_9P5o' \
        ''

# FUNCTIONS ____________________________________________________________________________________________________________


async def MakeCharacter(ctx : commands.Context):

    async def WaitForMsg(startingMsg, failMsg="Your answer is not valid.", answerEnum = None, condition=lambda m: True):

        if startingMsg != None and startingMsg != "":
            await ctx.send(startingMsg)

        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        answer = msg.content
        if condition(msg):
            if answerEnum != None:
                if answer in [e.name for e in answerEnum]:
                    a = eval(f'answerEnum.{answer}')
                    return a
            else:
                return answer

        await ctx.send(failMsg)
        await WaitForMsg("", failMsg, answerEnum, condition)

    racesStr = '\n'.join([r.name for r in Character.Races])
    professionsStr = '\n'.join([p.name for p in Character.Professions])

    newCharacter = Character.Character(
        await WaitForMsg("What is your character's name?"),
        # if the sexes ever change, change that although idk why would they change i mean what?
        await WaitForMsg("What is your character's sex?\npossible sexes are -\nmale\nfemale\nunknown", answerEnum=Character.Sexes),
        await WaitForMsg("What will your character's race be?\nPossible races are:\n" + racesStr, "Couldn't find that race.", Character.Races),
        await WaitForMsg("What will your character's profession be?\nPossible professions are:\n" + professionsStr, "Couldn't find that profession.", Character.Professions),
        await WaitForMsg("What is your character's backstory?")

    )

    return newCharacter

def UpdatePlayers():
    with open("Players.dat", 'wb') as f:

        dilldPlayers = {}

        for authorId, player in players.items():
            dilldPlayer = copy.copy(player)
            dilldPlayer.author = None
            dilldPlayer.Reset()
            dilldPlayers[authorId] = dilldPlayer

        dill.dump(dilldPlayers, f)

def LoadPlayers():

    with open('Players.dat', 'rb') as f:
        dilldPlayers = dill.load(f)

        newPlayers = {}
        for id, player in dilldPlayers.items():
            dilldPlayer = player
            dilldPlayer.author = bot.get_user(id)
            dilldPlayer.party = Player.Party([dilldPlayer])
            newPlayers[id] = dilldPlayer
        return newPlayers

def LoadAdventures():

    with open('Adventures.dat', 'rb') as f:
        adventures = dill.load(f)
        return adventures


# COMMANDS______________________________________________________________________________________________________________
players: Dict[int, Player.Player] = {}
adventures : List[Adventure.Adventure] = []

@bot.event
async def on_ready():
    print("ready")

    # PLAYERS_____________________________________________________________________________________________________________
    global players
    global adventures
    players = LoadPlayers()
    GlobalVars.players = players
    print("loaded players")
    adventures = LoadAdventures()
    print("loaded adventures")

    AddCurency(329960504376426496, 11)

@bot.command()
async def get_players(ctx : commands.Context):

    if len(players) > 0:
        playerNames = []
        for authorId, player in players.items():
            playerNames.append(bot.get_user(authorId) + " : " + player.nickname)

        await ctx.send(',\n'.join(playerNames))
    else:
        await ctx.send("no players were found.")



async def StartAdventure(channel, party, adventure : Adventure.Adventure):

    Playing = True

    async def PlayAdventure():
        await adventure.Init(channel, party)
        nonlocal Playing
        while Playing:
            msg : discord.Message = await bot.wait_for('message', check= lambda m : m.author.id in players and players[m.author.id] == adventure.currentPlayer)
            result = await adventure.ExecuteAction(msg.channel, msg.content, players[msg.author.id])
            #if not result:
            #    Playing = False

    async def ExecuteCommands():
        print("started executing commands")
        adventureCommands = []
        for c in adventure.commands:
            adventureCommands.append(c.name)
            adventureCommands.extend(c.aliases)

        while Playing:
            message: discord.Message = await bot.wait_for('message', check=lambda m: m.author.id in players and players[m.author.id] == adventure.currentPlayer
                                                      and m.content in adventureCommands)
            cmd = message.content
            msg = None
            if " " in cmd:
                cmd = cmd.split[' '][0]
                msg = msg.content.split[' '][1:]
            await adventure.ExecuteCommand(message.channel, cmd, players[message.author.id], None)

    await asyncio.gather(PlayAdventure(), ExecuteCommands())
    return

async def CommunityAdventures(channel : discord.TextChannel, player : Player.Player):

    adventuresPlayed = []
    party = player.party

    for p in party:
        adventuresPlayed.extend(p.adventuresPlayed)

    for a in adventures:
        if a not in adventuresPlayed:

            #for p in party:
            #    p.adventuresPlayed.appemd(a)

            await StartAdventure(channel, party, a)
            return

communityAdventures = Menu.Starter("Community Adventures", "🖐️", CommunityAdventures, 'play adventures made by the community')
computerAdventures = Menu.Starter("Computer Generated Adventure", "🦾", CommunityAdventures, 'play random-generated adventures.')
async def Pass():
    pass
adventureBuilder = Menu.Starter("Adventure Builder", "🛠️", Pass, 'Build your own adventures using the Adventure Builder tool!')

quickPlay = Menu.Menu("Quick Play", "➡️", [communityAdventures, computerAdventures], 'Quick random games by the community / computer generated')
campaign = Menu.Menu("Campaign", "🌍", [], 'explore the open world, play missions, and experience the `D&DISCORD` campaign.')
mainMenu = Menu.Menu("Main Menu", "🍆", [campaign, quickPlay, adventureBuilder])


#🌍
#🦾
#🖐️
#➡️
#🛠️

declineInvite = '⛔'
acceptInvite = '✅'

@bot.command(aliases=['play'])
async def start(ctx : commands.Context):
    if ctx.author.id in players.keys():
        await ctx.send(f"Welcome back {players[ctx.author.id].nickname}!")
        player = players[ctx.author.id]
        player.author = ctx.author
    else:
        await ctx.send(f"Welcome to the crew {ctx.author.name}")
        await asyncio.sleep(2)
        await ctx.send(f"Lets make your first character.")
        await asyncio.sleep(1.25)

        character = await MakeCharacter(ctx)
        player = Player.Player(ctx.author)
        players[ctx.author.id] = player
        GlobalVars.players[ctx.author.id] = player
        player.AddCharacter(character)
        player.SetCharacter(player.characters[0])
        UpdatePlayers()

    if player.party.partyLeader == player:
        await mainMenu.Send(ctx.channel, players[ctx.author.id])

    else:
        await ctx.send('you are not the leader of your party. only he can initiate the game.')


@bot.command()
async def debug(ctx):
    player = players[ctx.author.id]
    player.author = ctx.author

    await CommunityAdventures(ctx.channel, player)



# PARTY COMMANDS _______________________________________________________________________________________________________

@bot.command(aliases=['invite'])
async def inv(ctx : commands.Context, member : discord.Member):

    invitationTimeout = 300

    sender = players[ctx.author.id]

    if member != sender.author:

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
    else:
        await ctx.send('you can not invite yourself!')

@bot.command(aliases=['p'])
async def party(ctx):
    player = players[ctx.author.id]
    await ctx.send(", ".join([p.author.mention for p in player.party]))


@bot.command(aliases=['k'])
async def kick(ctx, member : discord.Member):
    player = players[ctx.author.id]
    if len(player.party) > 1 and player.party.partyLeader == player and member != player.author:
        player.party.Kick(players[member.id])

        await ctx.send(f"kicked {member.mention} from the party")
        await ctx.author.send(f"you have been kicked from {player.author.mention}'s party.")


@bot.command(aliases=['l'])
async def leave(ctx):
    player = players[ctx.author.id]
    if len(player.party) > 1 and player.party.partyLeader == player:
        player.party.Kick(player)

        await ctx.send(f"{ctx.author.mention} has left the party")
        await ctx.author.send(f"you have left {player.party.partyLeader.author.mention}'s party.")


bot.run(TOKEN)
