from __future__ import annotations
from typing import *
from Room import Room
from Functions import SpaceFunctionName
from Action import Action
from Player import Party, Player
import GlobalVars
import discord
from discord.ext import commands
#import nacl
import random
from itertools import cycle
import functools

class Command:
    def __init__(self, name, action, aliases=[]):
        self.name = name
        self.action : Action = action
        self.aliases = aliases

    async def __call__(self, channel : discord.TextChannel=None, executioner : Player = None):
        await self.action(channel, executioner)
        return not self.action.passTurn

class Adventure:

    def __init__(self, name, description, minPartySize, maxPartySize):

        self.name = name
        self.description = description
        self.rooms = []
        self.startRoom : Room = None

        self.minParty = minPartySize
        self.maxParty = maxPartySize

        for room in self.rooms:
            room.adventure = self

        self.commands : List[Command] = []

        self.useVoice = False

        @self.command(aliases=['inventory'])
        async def inv(ctx, players):
            """show yeer inv"""
            print("show inv")

        @self.command(aliases=['Toggle Voice'])
        async def ToggleVoice(channel, player):
            adventure = player.adventure
            if player.author.voice and player.author.voice.channel:
                await adventure.ToggleVoice(player.author.voice.channel)

        self.vars = {}
        self.party : Party = None

        self.playingBackgroundMusic = False
        self.backgroundTrack = ""

    async def Init(self, channel : discord.TextChannel, party : Party):

        if (len(party) >= self.minParty or self.minParty == 0) and (len(party) <= self.maxParty or self.minParty == 0):

            self.party = party

            self.playerTurns = cycle(random.sample(self.party.players.copy(), len(self.party)))
            self.currentPlayer = next(self.playerTurns)

            for p in self.party:
                p.adventure = self
                p.adventuresPlayed.add(self)

            if all([p.author.voice and p.author.voice.channel == self.party[0].author.voice.channel for p in self.party]):
                await self.ToggleVoice(self.party.partyLeader.author.voice.channel)
            else:
                await channel.send("Not all party members in same voice channel. this disables the use of sound "
                                   "in the adventure, which might limit your experience. are you sure you want to continue?"
                                   "\n1. connect voice to my channel\n2.continue without voice\n(answer with the number)")
                msg = await GlobalVars.bot.wait_for('message',
                                                    check= lambda m : m.author in [p.author for p in self.party] and
                                                                      ((m.content == '1' and m.author.voice and m.author.voice.channel) or (m.content == '2')))

                if int(msg.content) == 1:
                    await self.ToggleVoice(self.party.partyLeader.author.voice.channel)
                elif int(msg.content) == 2:
                    self.useVoice = False

            for i in range(len(self.party)):
                self.currentPlayer = next(self.playerTurns)
                self.startRoom.SilentEnter(self.currentPlayer)
            await self.startRoom.Enter(channel, self.currentPlayer)


        else:
            minPlayers = ("\n" + "minmum amount of players is " + str(self.minParty)) if self.minParty > 0 else ""
            maxPlayers = ("\n" + "maximum amount of players is " + str(self.maxParty)) if self.maxParty > 0 else ""
            raise Exception("The Party is not sized for this adventure." + minPlayers + maxPlayers)

    def AddCommand(self, command):
        self.commands.append(command)
        return command

    def RemoveCommandByName(self, commandName):
        for c in self.commands:
            if commandName in c.aliases + c:
                self.commands.remove(c)
                return c

    async def ExecuteAction(self, message : discord.Message, executioner : Player):
        cmd = message.content
        if executioner not in self.party:
            raise Exception(f"executioners of {cmd} command not in adventure party")
        player = self.party[message.author]
        room = player.character.room

        result = None

        if cmd.isnumeric():
            if int(cmd) - 1 <= len(room.actions) and int(cmd) >= 1:
                result = await room.actions[int(cmd) - 1](message.channel, executioner)


        for a in room.actions:
            if a.name == cmd:
                result = await a(message.channel, executioner)

        if result != None:

            if not result:
                self.currentPlayer = next(self.playerTurns)

            return result

    async def ExecuteCommand(self, command : discord.Message, executioner : Player):
        cmd = command.content
        for c in self.commands:
            commandNames = c.aliases + [c.name]
            if cmd in commandNames:
                await c(command.channel, executioner)

    async def ToggleVoice(self, voiceChannel : discord.VoiceChannel):

        self.useVoice = not self.useVoice
        if self.useVoice:
            voiceClient = await voiceChannel.connect()
            GlobalVars.botVoiceClients[voiceChannel.guild] = voiceClient

            if self.playingBackgroundMusic:
                await self.ResumeBackgroundMusic(voiceClient.guild)

        else:
            voiceClient = GlobalVars.botVoiceClients[voiceChannel.guild]
            await voiceClient.disconnect()
            GlobalVars.botVoiceClients.pop(voiceChannel.guild)

    def command(self, *, aliases: List[str] = [], condition: Callable[[], bool] = lambda: True, passTurn=False,
                failFeedback="You can not use this command right now."):

        def decorator(function):
            commandObj = Command(
                SpaceFunctionName(function.__name__),
                Action(function.__name__, function.__doc__, function, condition, passTurn, failFeedback),
                aliases
            )
            self.AddCommand(commandObj)
            return commandObj

        return decorator

    def AddRoom(self, room : Room):
        self.rooms.append(room)
        if self.startRoom == None:
            self.startRoom = room
        room.adventure = self
        return room

    def SetStartRoom(self, room : Room):
        if room in self.rooms:
            self.startRoom = room
            return room
        else:
            raise Exception("Start room not in list of rooms")

    def GetRoomByName(self, name):
        for r in self.rooms:
            if r.name == name:
                return r
            raise Exception("Room not found")

    def Reset(self):
        self.party = None

    def SetBackgroundMusic(self, guild, trackName):
        self.backgroundTrack = trackName
        self.playingBackgroundMusic = True
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[guild]
            if voiceClient.is_playing():
                voiceClient.stop()
            voiceClient.play(discord.FFmpegPCMAudio(trackName))

    def PauseBackgroundMusic(self, guild):
        self.playingBackgroundMusic = False
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[guild]
            voiceClient.stop()

    def ResumeBackgroundMusic(self, guild):
        self.playingBackgroundMusic = True
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[guild]
            voiceClient.play(discord.FFmpegPCMAudio(self.backgroundTrack))

    def StopBackgroundMusic(self, guild):
        self.backgroundTrack = ""
        self.playingBackgroundMusic = False
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[guild]
            voiceClient.stop()
