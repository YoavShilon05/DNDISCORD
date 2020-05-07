from discord.ext import commands
import Adventure
import Room
import Action
import Player
import Character

bot = commands.Bot(command_prefix="d.")
TOKEN = 'NzA2MjE2OTkxMDA1ODY4MDgz.XrLYFg.VH2-yjc2EPx_Nv9QmFCFuz_9P5o' \
        ''


# ROOMS ________________________________________________________________________________________________________________
room1 = Room.Room('room1','yeer in room 1, take a seat', 'room1')
room2 = Room.Room('room1','yeer in room 2, take a seat', 'room2')

# ACTIONS ______________________________________________________________________________________________________________


adv = Adventure.Adventure("DEMO ADVENTURE", 'idk just a demo', [room1, room2])

@room1.action()
async def MoveToRoom2(ctx, players : Player.Player):
    await room2.Enter(ctx, players)

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
    await adv.ExecuteCommand(ctx, msg, [player])

bot.run(TOKEN)