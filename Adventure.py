from __future__ import annotations
from typing import *
from Room import Room, CapStrToSpaced
from Action import Action
from Player import Party, Player


class Command:
    def __init__(self, name, action, aliases=[]):
        self.name = name
        self.action = action
        self.aliases = aliases

    async def __call__(self, *args):
        await self.action(*args)

class Adventure:

    def __init__(self, name, description, rooms : List[Room], startRoom : Room or None = None):

        self.name = name
        self.description = description
        self.rooms = rooms
        self.startRoom = startRoom if startRoom is not None else rooms[0]

        self.commands : List[Command] = []

        @self.command()
        async def inv(ctx, player):
            """show yeer inv"""
            await ctx.send(player.character.inventory)


        self.party : Party or None = None

    async def Init(self, ctx, party : Party):
        self.party = party
        await self.startRoom.Enter(ctx, party.players)

    def AddCommand(self, command):
        self.commands.append(command)

    def RemoveCommandByName(self, commandName):
        for c in self.commands:
            if c.name == commandName:
                self.commands.remove(c)
                return

    async def ExecuteCommand(self, ctx, cmd : str, executioners : List[Player]):
        for e in executioners:
            if e not in self.party:
                raise Exception(f"executioners of {cmd} command not in adventure party")
        player = self.party[ctx.author]
        room = player.character.room

        if cmd.isnumeric():
            if int(cmd) - 1 <= len(room.actions):
                await room.actions[int(cmd) - 1](ctx, executioners)

        for a in room.actions:
            if a.name == cmd:
                await a(ctx, executioners)
                return

        for c in self.commands:
            commandNames = c.aliases.copy()
            commandNames.append(c.name)
            if cmd in commandNames:
                await c(ctx, executioners)
                return

        raise ValueError(f"{cmd} is not a valid command")

    def command(self, *, aliases: List[str] = []):

        def decorator(function):
            commandObj = Command(
                CapStrToSpaced(function.__name__),
                Action(function.__name__, function.__doc__, function),
                aliases
            )
            self.AddCommand(commandObj)
            return commandObj

        return decorator



