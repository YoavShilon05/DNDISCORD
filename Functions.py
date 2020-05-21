from __future__ import annotations
from typing import *
from inspect import getfullargspec
import Action

if TYPE_CHECKING:
    import Player
    import Room




def ConnectRooms(room1 : Room.Room, room2 : Room.Room):
    def AddRoomEnterAction(firstRoom, secondRoom):
        async def Function(channel, player):
            await secondRoom.Enter(channel, player)
        action = Action.Action(f"go to {secondRoom.name}", "", Function)
        firstRoom.AddAction(action)
    AddRoomEnterAction(room1, room2)
    AddRoomEnterAction(room2, room1)

def SpaceFunctionName(name : str):

    #newStr starts with a colon to allow to index it.
    #wil be replaced in return.
    '''
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
    '''


    return name.lower().replace('_', ' ')

async def CallAction(action : Callable, channel, executioner : Player.Player, message : str):
    if len(getfullargspec(action).args) == 0:
        await action()
    elif len(getfullargspec(action).args) == 1:
        await action(channel)
    elif len(getfullargspec(action).args) == 2:
        await action(channel, executioner)
    elif len(getfullargspec(action).args) == 3:
        await action(channel, executioner, message)