from typing import *
from Room import Room
from Action import ExecuteAction
from Player import Party

class Command:
    def __init__(self, name, action):
        self.name = name
        self.action = action
    def Execute(self, ctx, executioners):
        ExecuteAction(self.action, ctx, executioners)

class Adventure:

    def __init__(self, name, description, rooms : List[Room], startRoom : Room):

        self.name = name
        self.description = description
        self.rooms = rooms
        self.startRoom = startRoom
        self.commands : List[Command] = []

        self.party : Party or None = None

    def SetParty(self, party : Party):
        self.party = party

    async def Init(self, ctx, players):
        await self.startRoom.Enter(ctx, players)

    def AddCommand(self, command):
        self.commands.append(command)

    def RemoveCommandByName(self, commandName):
        for c in self.commands:
            if c.name == commandName:
                self.commands.remove(c)
                return

    async def ExecuteCommand(self, ctx, cmd):
        player = self.party[ctx.author]
        room = player.character.currentRoom
        for a in room.actions:
            if a.name == cmd:
                await ExecuteAction(a, ctx, [player])
                return

        for c in self.commands:
            if c.name == cmd:
                action = c.action
                await ExecuteAction(action, ctx, [player])
                return

        raise Exception(f"no {cmd} command found.")