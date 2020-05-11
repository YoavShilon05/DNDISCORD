from discord.ext import commands
import GlobalVars
bot = commands.Bot(command_prefix="d.")
GlobalVars.bot = bot
from Functions import *
import Adventure
import Room
import Player
import Character
import Sequence
import Action
TOKEN = 'NzA2MjE2OTkxMDA1ODY4MDgz.XrLYFg.VH2-yjc2EPx_Nv9QmFCFuz_9P5o' \
        ''

adv = Adventure.Adventure("DEMO ADVENTURE", 'idk just a demo')


# ROOMS ________________________________________________________________________________________________________________
room1 = Room.Room('room1', Sequence.Sequence(['you are in room 1', ("theres a brown table and two chairs", 'Smash Mouth - All Star.mp3')], deleteMessages=False), Sequence.Sequence([('room 1', 1)], deleteMessages=False))
room2 = Room.Room('room2', Sequence.Sequence([('you are in room 2', 'Smash Mouth - All Star.mp3', 1.5), ("theres a blue table and five chairs", 'Smash Mouth - All Star.mp3', 1.5)], deleteMessages=False), Sequence.Sequence(['room 2']))
room3 = Room.Room('room3', Sequence.Sequence([('you are in room 3', 1.5), ('idk what to put here.', 1.5)], deleteMessages=False), Sequence.Sequence([('room 3', 1)], deleteMessages=False))
# ACTIONS ______________________________________________________________________________________________________________


ConnectRooms(room1, room2)
ConnectRooms(room1, room3)
ConnectRooms(room2, room3)


@adv.command()
async def tst(ctx):
    await ctx.send("test is working")


@bot.event
async def on_ready():
    print("ready")

@bot.command()
async def set(ctx):
    player = Player.Player(ctx.author)
    player.AddCharacter(Character.Character('sambady', Character.Sexes.male, Character.Races.Elf, Character.Professions.Archer, "idk its just a test bru"))
    ### dont do dat VV
    player.character = player.characters[0]
    global party
    party = Player.Party([player])
    await adv.Init(ctx, party)


@bot.command()
async def cmd(ctx, *, msg):
    player = party[ctx.author]
    await adv.ExecuteCommand(ctx, msg, player)

bot.run(TOKEN)