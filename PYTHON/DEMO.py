from discord.ext import commands
import GlobalVars
import dill

bot = commands.Bot(command_prefix="d.")
GlobalVars.bot = bot

from Adventure import Adventure, Room, Action, Sequence, SequenceItem, Command
from Character import Character, Sexes, Races, Professions, PersonalityPoints, MakePersonalityPoints, Item, Usable, Battle
from Player import Player, Party

async def appleFunc(player):
    player.character.AddHealth(5)

async def posionFunc(player):
    player.character.AddHealth(-6)

apple = Usable("apple", "apple", appleFunc)
poison = Usable('poison', 'poison', posionFunc)
adv = Adventure("DEMO ADVENTURE", 'idk just a demo', None,  0, 0, subtitle="the demo")


# ROOMS ________________________________________________________________________________________________________________
room1 = Room('room1', Sequence([
    SequenceItem("this is room 1"),
    SequenceItem("it has two tables and five chairs")
]))
room2 = Room('room2', Sequence([
    SequenceItem("this is room 2"),
    SequenceItem("idk what to put here")
]))
room3 = Room('room3', Sequence([
    SequenceItem("this is room 3"),
    SequenceItem("idk what to put here")
]))

goblin = Character("goblin", Sexes.male, Races.goblin, Professions.none)
battle = Battle([goblin])
battleRoom = Room('training room', Sequence([]), battle=battle)


room1.SetConnections([room2, room3])
room2.SetConnections([room3, room1])
room3.SetConnections([room1, room2, battleRoom])
battleRoom.SetConnections([room3])

@room1.action()
async def on_enter(player):
    """start playin music"""
    player.adventure.SetBackgroundMusic('neverGonnaGiveYouUp.mp3')

@room1.action()
async def StopMusic(player):
    """stop the bg music"""
    player.adventure.StopBackgroundMusic()
    return False

stopMusic = room1.GetActionByName('StopMusic')

@stopMusic.Condition
def StopMusicCondition(player):
    return player.character.room.adventure.GetRoomByName("room2").entered


@adv.command()
async def tst(player, msg):
    await player.adventure.channel.send("test is working")

adv.rooms = [room1, room2, room3]

with open('Adventures.dat', 'wb') as f:
    dill.dump([adv], f)