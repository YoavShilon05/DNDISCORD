from discord.ext import commands
import GlobalVars
bot = commands.Bot(command_prefix="d.")
GlobalVars.bot = bot

import Functions
import Adventure
import Room
import Sequence
import dill
import Item
import Shop

def appleFunc(channel, player):
    player.character.AddHealth(5)

def posionFunc(channel, player):
    player.character.AddHealth(-6)

apple = Item.Usable("apple", "apple", appleFunc)
poison = Item.Usable('poison', 'poison', posionFunc)

adv = Adventure.Adventure("DEMO ADVENTURE", 'idk just a demo', 0, 0)


# ROOMS ________________________________________________________________________________________________________________
room1 = Room.Room('room1', Sequence.Sequence(['you are in room 1', "theres a brown table and two chairs"], deleteMessages=False), Sequence.Sequence([('room 1', 1)], deleteMessages=False), [apple])
room2 = Room.Room('room2', Sequence.Sequence([('you are in room 2', 1.5), ("theres a blue table and five chairs", 1.5)], deleteMessages=False), Sequence.Sequence(['room 2']))
room3 = Room.Room('room3', Sequence.Sequence([('you are in room 3', 1.5), ('idk what to put here.', 1.5)], deleteMessages=False), Sequence.Sequence([('room 3', 1)], deleteMessages=False))

shop = Room.Shop('da shop', Sequence.Sequence([]), room1, [(apple, 5, 23), (poison, 5, 15)])

Functions.ConnectRooms(room1, room2)
Functions.ConnectRooms(room1, room3)
Functions.ConnectRooms(room2, room3)


adv.AddRoom(room1)
adv.AddRoom(room2)
adv.AddRoom(room3)



@room1.action()
async def on_enter(channel, player):
    """start playin music"""
    player.adventure.SetBackgroundMusic(channel.guild, 'neverGonnaGiveYouUp.mp3')

@room1.action()
async def StopMusic(channel, player):
    """stop the bg music"""
    adv : Adventure.Adventure = player.adventure
    adv.StopBackgroundMusic(channel.guild)

stopMusic = room1.GetActionByName('StopMusic')

@stopMusic.Condition
def StopMusicCondition(action):
    return action.room.adventure.GetRoomByName("room2").entered


adv.SetStartRoom(room1)


@adv.command()
async def tst(ctx):
    await ctx.send("test is working")


with open('Adventures.dat', 'wb') as f:
    dill.dump([adv], f)