from __future__ import annotations
from typing import *

import GlobalVars
import discord
import random
from itertools import cycle
import Action
import asyncio

if TYPE_CHECKING:
    import Room
    import Player


class Command:
    def __init__(self, name, action, aliases=[]):
        self.name = name
        self.action : Action.Action = action
        self.aliases = aliases

    async def __call__(self, channel : discord.TextChannel, executioner : Player.Player, message=None):
        await self.action(channel, executioner, message)
        return self.action.passTurn


class Adventure:

    def __init__(self, name, description, minPartySize, maxPartySize):

        self.name = name
        self.description = description
        self.rooms = []
        self.startRoom : Room.Room = None

        self.minParty = minPartySize
        self.maxParty = maxPartySize

        self.maker = None

        for room in self.rooms:
            room.adventure = self

        self.commands : List[Command] = []

        self.useVoice = False

        @self.command(aliases=['inventory'])
        async def inv(channel, player, item):
            """show yeer inv"""

            msg = "Inventory\n"
            if item == None:
                await channel.send(msg + player.character.inventory.Preview())
            else:
                if item.lower() in [i.name.lower() for i in player.character.room.items]:
                    await channel.send(msg + player.character.room.GetItemByName(item).Preview())
                else:
                    await channel.send(msg + "no item by that name was found")

        @self.command(aliases=['Toggle Voice'])
        async def toggle_voice(channel, player):
            adventure = player.adventure
            if player.author.voice and player.author.voice.channel:
                await adventure.ToggleVoice(player.author.voice.channel)

        @self.command(aliases=['s', 'show_stats'])
        async def stats(channel, player):

            await channel.send(
                f'''health : {player.character.health}

                '''
            )


        self.vars = {}
        self.party : Player.Party = None

        self.playingBackgroundMusic = False
        self.backgroundTrack = ""

    def SetMaker(self, maker : Player.Player):
        self.maker = maker

    async def Init(self, channel : discord.TextChannel, party : Player.Party):

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

    async def ExecuteAction(self, channel, action : str, executioner : Player.Player):

        if executioner not in self.party:
            raise Exception(f"executioners of {action} command not in adventure party")

        room = executioner.character.room

        passTurn = None

        if action.isnumeric():
            if int(action) - 1 <= len(room.actions) and int(action) >= 1:
                passTurn = await room.numberedActions[int(action) - 1](channel, executioner)

        if passTurn == None:
            for a in room.actions:
                if a.name == action:
                    passTurn = await a(channel, executioner)


        if type(passTurn) == bool:
            if not passTurn:
                self.currentPlayer = next(self.playerTurns)
                await channel.send(f"turn passes to {self.currentPlayer.author.mention}.\n What will you do?")
                await asyncio.sleep(2)
                await channel.send(self.currentPlayer.character.room.GetActionRepr())

        return len(room.actions) > 0

    async def ExecuteCommand(self, channel, command : str, executioner : Player.Player, message : str):

        for c in self.commands:
            commandNames = c.aliases + [c.name]
            if command in commandNames:
                await c(channel, executioner, message)

    async def ToggleVoice(self, voiceChannel : discord.VoiceChannel):

        self.useVoice = not self.useVoice
        if self.useVoice:
            voiceClient = await voiceChannel.connect()
            GlobalVars.botVoiceClients[voiceChannel.guild.id] = voiceClient

            if self.playingBackgroundMusic:
                self.ResumeBackgroundMusic(voiceClient.guild)

        else:
            voiceClient = GlobalVars.botVoiceClients[voiceChannel.guild.id]
            await voiceClient.disconnect()
            GlobalVars.botVoiceClients.pop(voiceChannel.guild.id)

    def command(self, *, aliases: List[str] = [], passTurn=False):

        def decorator(function):
            commandObj = Command(
                function.__name__,
                Action.Action(function.__name__, function.__doc__, function, passTurn),
                aliases,
            )

            self.AddCommand(commandObj)
            return commandObj

        return decorator

    def AddRoom(self, room : Room.Room):
        self.rooms.append(room)
        if self.startRoom == None:
            self.startRoom = room
        room.adventure = self
        return room

    def SetStartRoom(self, room : Room.Room):
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
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[guild.id]
            if voiceClient.is_playing():
                voiceClient.stop()
            voiceClient.play(discord.FFmpegPCMAudio(trackName))

    def PauseBackgroundMusic(self, guild):
        self.playingBackgroundMusic = False
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[guild.id]
            voiceClient.stop()

    def ResumeBackgroundMusic(self, guild):
        self.playingBackgroundMusic = True
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[guild.id]
            voiceClient.play(discord.FFmpegPCMAudio(self.backgroundTrack))

    def StopBackgroundMusic(self, guild):
        self.backgroundTrack = ""
        self.playingBackgroundMusic = False
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[guild.id]
            voiceClient.stop()

    def End(self):

        for p in self.party:
            p.character.room = None