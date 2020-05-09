from __future__ import annotations
from typing import *
from Room import Room, CapStrToSpaced
from Action import Action
from Player import Party, Player
import GlobalVars
import discord
from discord.ext import commands
import nacl

class Command:
    def __init__(self, name, action, aliases=[]):
        self.name = name
        self.action : Action = action
        self.aliases = aliases

    async def __call__(self, ctx : commands.Context=None, executioner : Player = None):
        await self.action(ctx, executioner)

class Adventure:

    def __init__(self, name, description, rooms : List[Room], startRoom : Room = None):

        self.name = name
        self.description = description
        self.rooms = rooms
        self.startRoom = startRoom if startRoom is not None else rooms[0]

        for room in self.rooms:
            room.adventure = self

        self.commands : List[Command] = []

        self.useVoice = False
        self.adventure = None
        @self.command(aliases=['inventory'])
        async def inv(ctx, players):
            """show yeer inv"""

        @self.command()
        async def ToggleVoice(ctx : commands.Context, player):
            adventure = player.adventure
            adventure.ToggleVoice(ctx)

        self.vars = {}
        self.party : Party = None

    async def Init(self, ctx, party : Party):
        self.party = party

        for p in self.party:
            p.adventure = self

        if all(p.author.voice and p.author.voice.channel == self.party[0].author.voice.channel for p in self.party):
            await self.ToggleVoice(ctx)
        else:
            await ctx.send("Not all party members in same voice channel. this disables the use of sound "
                           "in the adventure, which will limit your experience. are you sure you want to continue?"
                           "\n1. connect voice\n2.continue without voice\n(answer with the number)")
            msg = await GlobalVars.bot.wait_for('message', check= lambda m : m.author in [p.author for p in self.party] and m.content.isnumeric and int(m.content) in [1, 2])

            if int(msg.content) == 1:
                await self.ToggleVoice(ctx)
            elif int(msg.content) == 2:
                self.useVoice = False


        await self.startRoom.Enter(ctx, party.players)

    def AddCommand(self, command):
        self.commands.append(command)

    def RemoveCommandByName(self, commandName):
        for c in self.commands:
            if commandName in c.aliases + c:
                self.commands.remove(c)
                return

    async def ExecuteCommand(self, ctx, cmd : str, executioner : Player):
        if executioner not in self.party:
            raise Exception(f"executioners of {cmd} command not in adventure party")
        player = self.party[ctx.author]
        room = player.character.room

        if cmd.isnumeric():
            if int(cmd) - 1 <= len(room.actions) and int(cmd) >= 1:
                await room.actions[int(cmd) - 1](ctx, executioner)
                return

        for a in room.actions:
            if a.name == cmd:
                await a(ctx, executioner)
                return

        for c in self.commands:
            commandNames = c.aliases + [c.name]
            if cmd in commandNames:
                await c(ctx, executioner)
                return

        raise ValueError(f"{cmd} is not a valid command")

    async def ToggleVoice(self, ctx : commands.Context):
        player = self.party[ctx.author]
        player.adventure.useVoice = not player.adventure.useVoice
        if player.adventure.useVoice:
            voiceClient = await ctx.author.voice.channel.connect()
            GlobalVars.botVoiceClients[ctx.guild] = voiceClient
        else:
            await ctx.voice_client.disconnect()
            GlobalVars.botVoiceClients.pop(ctx.guild)

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



