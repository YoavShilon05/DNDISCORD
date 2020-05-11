from  __future__ import annotations
from typing import *
from inspect import getfullargspec
import discord
if TYPE_CHECKING:
    from Room import Room
    from Action import Action
    from Player import Player

def ConnectRooms(room1 : Room, room2 : Room):
    def AddAction(room1, room2):
        async def Function(ctx, player):
            await room2.Enter(ctx, [player])
        action = Action(f"go to {room2.name.lower()}", "", Function)
        room1.AddAction(action)
    AddAction(room1, room2)
    AddAction(room2, room1)

def SpaceFunctionName(name : str):

    #newStr starts with a colon to allow to index it.
    #wil be replaced in return.
    newStr = ":"

    for i in range(len(name)):
        l = name[i]
        if newStr[-1] == " ":
            newStr += l.lower()
        else:
            if l.isupper() or l.isnumeric():
                newStr += " " + l.lower() if i != 0 else l.lower()
            elif l == '_' or l == '-':
                newStr += " "
            else:
                newStr += l

    return newStr[1:]


async def CallAction(action : Callable, message : discord.Message, executioner : Player):
    if len(getfullargspec(action).args) == 0:
        await action()
    elif len(getfullargspec(action).args) == 1:
        await action(message)
    elif len(getfullargspec(action).args) == 2:
        await action(message, executioner)