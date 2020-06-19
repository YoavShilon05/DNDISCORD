
"""this file contains classes that build up the adventure and the world surrounding it."""

from __future__ import annotations
from typing import *
import GlobalVars
import discord
import random
from itertools import cycle
import asyncio
import Player
import Character
import copy
from collections import deque

class Action:

    """An action that can be executed by the player if in the room containing it."""

    def __init__(self, name : str, description : str, action : Callable, condition= lambda p : True):
        self.name : str = name
        self.description : str = description
        self.action : Callable[[Player.Player], Awaitable[bool]] = action
        self.condition : Callable[[Player.Player], bool] = condition

    async def __call__(self, executioner : Player.Player) -> bool:

        if self.condition(executioner):
            return await self.action(executioner)
        else:
            return False

    def Condition(self, foo):
        self.condition = foo


sfx = {
    #add sfx here
}

passEmoji = '▶️'
endEmoji = "💠"

class SequenceItem:
    def __init__(self, content : str, *, useReaction : bool = True, delay : float = 0, delete : bool = False,
                 track : str = None):
        self.content : str = content
        self.useReaction : bool = useReaction
        self.delay : float = delay
        self.delete : bool = delete
        self.track : str = track

class Sequence:
    """a sequence of text that will be sent on the channel."""
    def __init__(self, items : List[SequenceItem]):
        self.waitForReaction : bool = True
        self.sequence : List[SequenceItem] = items
        self.room : Room = None

    async def Play(self):

        playedMusic = False
        for i in range(len(self.sequence)):

            item = self.sequence[i]

            msg : discord.Message = await self.room.adventure.channel.send(item.content)

            if item.track != None:
                if self.room.adventure.playingBackgroundMusic:
                    self.room.adventure.PauseBackgroundMusic()
                voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[self.room.adventure.channel.guild.id]
                voiceClient.play(discord.FFmpegPCMAudio(item.track))
                playedMusic = True

            if item.useReaction:
                if i == len(self.sequence):
                    await msg.add_reaction(endEmoji)
                else:
                    await msg.add_reaction(passEmoji)

                await GlobalVars.bot.wait_for('reaction_add', check=lambda r, u : ((r.emoji == passEmoji) and
                        (i != len(self.sequence)) and not u.bot or (r.emoji == endEmoji and i == len(self.sequence))))

            else:
                await asyncio.sleep(item.delay)

            if item.delete:
                await msg.delete()

        adventure = self.room.adventure

        if playedMusic:
            adventure.ResumeBackgroundMusic()

class Command:
    """commands are actions that could be executed at all times by the player, no conditions."""
    def __init__(self, name : str, description : str, action : Callable[[Player.Player, str], Awaitable[bool]], aliases : List[str] = []):
        self.name : str = name
        self.description : str = description
        self.command : Callable[[Player.Player, str], Awaitable[bool]] = action
        self.aliases : List[str] = aliases

    async def __call__(self, executioner : Player.Player, message : str = None) -> bool:
        passTurn = await self.command(executioner, message)
        return passTurn

class Room:

    """Rooms are the building blocks of the adventure.
    each rooms contains a list of actions that can be executed by the player and other data."""

    def __init__(self, name : str, description : Sequence, shortDescription : Sequence = None,
                 cutScene : Sequence = None, items : List[Character.Item] = [], battle : Character.Battle=None):

        self.name : str = name
        self.description : Sequence = description
        self.description.room = self
        self.shortDescription : Sequence = shortDescription
        if self.shortDescription == None:
            self.shortDescription = copy.copy(self.description)
        self.shortDescription.room = self
        self.actions : List[Action] = []

        self.adventure : Adventure = None
        self.players: List[Player.Player] = []
        self.entered : bool = False
        self.left : bool = False

        async def empty(player):
            return False

        self.onEnter : Callable[[Player.Player], Awaitable[bool]] = empty
        self.onLeave : Callable[[Player.Player], Awaitable[bool]] = empty

        self.items : List[Character.Item] = items
        self.battle = battle
        self.cutScene = cutScene

        self.executionOrder : Dict[int, Callable[[], Awaitable[None]]] = {}
        self.SetExecutionOrder(0, 1, 2)

    def RemoveItemByName(self, item : Character.Item) -> None:
        for i in self.items:
            if i.name == item:
                self.items.remove(i)

    async def Enter(self, player : Player.Player) -> None:

        self.players.append(player)

        if player.character.room != None:
            await player.character.room.Leave(player)

        player.character.room = self
        await self.onEnter(player)

        for i in range(len(self.executionOrder.keys())):
            await self.executionOrder[i]()

        await self.adventure.channel.send(self.GetActionRepr(player))

    def SilentEnter(self, player : Player.Player) -> None:
        if player.character.room != None:
            player.character.room.SilentLeave(player)
        self.players.append(player)
        player.character.room = self

    async def Leave(self, player : Player.Player) -> None:
        self.players.remove(player)
        player.character.room = None

        self.left = True

        await self.onLeave(player)

    def SilentLeave(self, player : Player.Player) -> None:
        self.players.remove(player)
        player.character.room = None

    def GetActionByName(self, name : str) -> Action:

        for a in self.actions:
            if a.name == name:
                return a

    def GetActionRepr(self, player : Player.Player) -> str:

        actionsStr = ""
        spacesToDescription = 8

        if len(self.actions) > 0:
            actionsStr = 'possible actions:\n'

            for i in range(len(self.actions)):
                a = self.actions[i]
                if a.condition(player):
                    actionsStr += f"{i + 1}. {a.name}{(spacesToDescription * ' - ' + a.description) if a.description != None and a.description != '' else ''}" + "\n"

        if len(self.items) > 0:
            actionsStr += "items:\n"
            for i in self.items:
                actionsStr += i.name + (spacesToDescription * ' - ' + i.description) if i.description != None and i.description != '' else '' + "\n"

        return actionsStr

    async def ExecuteAction(self, player : Player.Player, action : str) -> bool:

        if action.isnumeric():
            return await self.actions[int(action) - 1](player)

        else:

            for a in self.actions:
                if action == a.name:
                    return await a(player)

            for i in self.items:
                if action == i.name:
                    self.items.remove(i)
                    player.character.inventory.AddItem(i)
                    return False

    def action(self, condition = lambda p : True):

        def decorator(foo : Callable[[Player.Player], Awaitable[bool]]):

            if foo.__name__== "on_enter":
                self.onEnter = foo
            elif foo.__name__== "on_leave":
                self.onLeave = foo
            else:
                act = Action(foo.__name__.replace("_", " "), foo.__doc__, foo, condition)
                self.actions.append(act)

        return decorator

    def SetConnections(self, rooms : List[Room]):

        def AddRoomEnterAction(root, branch):
            async def Function(player):
                await branch.Enter(player)

            action = Action(f"go to {branch.name}", "", Function)
            root.actions.append(action)

        for r in rooms:
            AddRoomEnterAction(self, r)

    def SetExecutionOrder(self, cutSceneIndex : int, battleIndex : int, descriptionIndex : int):

        # check if indexes are 0, 1 and 2.
        indexes = [0, 1, 2]
        for i in [cutSceneIndex, battleIndex, descriptionIndex]:
            if i not in indexes:
                raise IndexError("index list must contain only 0, 1 and 2")
            else:
                indexes.remove(i)


        async def PlayDescription():
            if not self.entered:
                self.entered = True
                await self.description.Play()
            else:
                await self.shortDescription.Play()

        async def StartBattle():
            if self.battle != None:
                characters = []
                for p in self.players:
                    characters.append(p.character)
                await self.battle.Init(characters)

        async def PlayCutScene():
            if self.cutScene != None:
                await self.cutScene.Play()

        self.executionOrder = {
            cutSceneIndex: PlayCutScene,
            battleIndex: StartBattle,
            descriptionIndex: PlayDescription
        }


    #async def ExecuteAction(self, player, action : str):

    #    if action.isnumeric():
    #        return await self.actions[int(action) + 1](player)

    #    else:
    #        for a in self.actions:
    #            if a.name == action:
    #                return await a(player)

class Battle:

    def __init__(self, enemies : List[Character.Character]):

        self.heroes : List[Character.Character] = []
        self.enemies : List[Character.Character] = enemies

        self.heroCycle : cycle = cycle([])
        self.currentHero : Character = None
        self.loot = []

        for e in self.enemies:
            self.loot.extend(e.inventory.items)

        self.room : Room = None

    async def Init(self, heroes : List[Character.Character]):
        self.heroes = heroes

        self.heroCycle = cycle(self.heroes)
        self.PassTurn()

        while len(self.enemies) > 0:
            await self.Act(self.currentHero)

        self.room.items.extend(self.loot)


    def PassTurn(self):
        self.currentHero = next(self.heroCycle)

    async def Act(self, actor : Character.Character):

        if actor.player != None:

            channel : discord.TextChannel = actor.player.adventure.channel

            async def Attack(attacker : Character):
                await channel.send("enemies:\n" + "\n".join([e.name for e in self.enemies]))
                msg = await GlobalVars.bot.wait_for('message', check=lambda m : m.author == attacker.player.author and
                                                                                m.content in [e.name for e in self.enemies])

                enemy = [e for e in self.enemies if e.name == msg.content][0]
                damage = await attacker.Attack(enemy)
                if enemy.dead:
                    self.enemies.remove(enemy)
                    await channel.send(f"killed {enemy.name}")
                else:
                    await channel.send(f"dealt {damage} damage to {enemy.name}.")

            async def Pass(character : Character.Character):
                pass

            possibleMoves = {
                "attack" : Attack,
                "pass" : Pass
            }

            await channel.send("possible moves:\n" + "\n".join(possibleMoves.keys()))
            msg = await GlobalVars.bot.wait_for('message', check=lambda m : m.content in possibleMoves.keys() and m.author == actor.player.author)

            await possibleMoves[msg.content](actor)
            self.PassTurn()


#SHOP -- IDEA SCRAPPED FOR NOW.
"""
class _ShopItem:

    def __init__(self, item, price, stock):
        self.item : Character.Item = item
        self.price : float = price
        self.stock : int = stock
"""
"""
class Shop(Room):

    def __init__(self, name, description : Sequence, room, items : List[_ShopItem]):
        self.itemsOnOffer = items.copy()

        # room init does not support shop item handling.
        super().__init__(name, description, description, [])

        # shop item handler

        for i in items:
            self.AddItem(i.item, i.price, i.)

        Functions.ConnectRooms(room, self)

    def GetActionRepr(self, player : Player.Player):

        spaces = 8
        actionStr = "Shop:\n"
        for a in self.itemsOnOffer:
            actionStr += a.item.name + " " + a[0].name + spaces * " - " + str(a[1]) + "$"

    def AddItem(self, item, price, stock):

        self.itemsOnOffer.append(_ShopItem(item, price, stock))
        self.items.append(item)

        async def BuyItem(channel, player):
            if player.character.currency >= price:
                await channel.send(f"{player.character.name} has bought {'a' if item.name[0].islower() else 'an'} {item.name}")
                player.character.inventory.AddItem(item)
                # decrease the stock of the item by one

                itemOnStock = self.GetItemOnStockByName(item.name)
                itemOnStock[2] -= 1
                if itemOnStock[2] <= 0:
                    self.RemoveItem(item)

        action = Action.Action(item.name.lower(), item.description, BuyItem)

        self.AddAction(action)
        self._itemActions.append(action)

    def GetItemOnStockByName(self, name):
        for a in self.itemsOnOffer:
            if a[0].name == name:
                return a
        raise IndexError("item not found")
"""
"""
class  RoomNode:

    def __init__(self, data : Room, parent):
        self.data : Room = data
        self.parent : RoomNode = parent
        self.neighbors : List[RoomNode] = []

        if self.parent != None:
            self.parent.neighbors.append(self)


    def ToDict(self):
        d = {}
        d[self] = [n.ToDict() for n in self.neighbors]

        return d

    def __iter__(self):
        for b in self.neighbors:
            yield b
            b.__iter__()

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)
"""

class Adventure:

    """contains data on the class and all of the rooms that build it up.
    also contains methods that can be executed on the adventure."""

    def __init__(self, name : str, description : str, author : Player.Player, minPartySize : int, maxPartySize : int, rooms : List[Room] = None, subtitle : str = "") -> None:

        self.name : str = name
        self.subtitle : str = subtitle
        self.description : str = description
        self.rooms : List[Room] = rooms
        self.startRoom : Room = None

        self.minParty : int = minPartySize
        self.maxParty : int = maxPartySize

        self.author : Player.Player = author

        self.commands : List[Command] = []

        self.useVoice : bool = False


        @self.command(aliases=['inventory'])
        async def inv(player, item):
            """show yeer inv"""

            msg = "Inventory\n"
            if item == None:
                await player.adventure.channel.send(msg + player.character.inventory.Preview())
            else:
                if item.lower() in [i.name.lower() for i in player.character.room.items]:
                    await player.adventure.channel.send(msg + player.character.room.GetItemByName(item).Preview())
                else:
                    await player.adventure.channel.send(msg + "no item by that name was found")

        @self.command(aliases=['Toggle Voice'])
        async def toggle_voice(player):
            adventure = player.adventure
            if player.author.voice and player.author.voice.channel:
                await adventure.ToggleVoice(player.author.voice.channel)

        @self.command(aliases=['s', 'show_stats'])
        async def stats(player, msg):

            await player.adventure.channel.send(
                f'''health : {player.character.health}

                '''
            )


        self.vars : Dict[str, object] = {}
        self.party : Player.Party = None

        self.playingBackgroundMusic : bool = False
        self.backgroundTrack : str = ""

        self.channel : discord.TextChannel = None

    async def Init(self, channel : discord.TextChannel, party : Player.Party) -> None:

        self.channel = channel
        self.startRoom = self.rooms[0]
        for r in self.rooms:
            r.adventure = self

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
                await self.channel.send("Not all party members in same voice channel. this disables the use of sound "
                                   "in the adventure, which might limit your experience. are you sure you want to continue?"
                                   "\n1. connect voice to my channel\n2.continue without voice\n(answer with the number)")
                msg = await GlobalVars.bot.wait_for('message',
                                                    check= lambda m : (m.author in [p.author for p in self.party]) and
                                                                      ((m.content == '1' and m.author.voice and m.author.voice.channel) or (m.content == '2')))

                if int(msg.content) == 1:
                    await self.ToggleVoice(self.party.partyLeader.author.voice.channel)
                elif int(msg.content) == 2:
                    self.useVoice = False

            for i in range(len(self.party)):
                self.currentPlayer = next(self.playerTurns)
                self.startRoom.SilentEnter(self.currentPlayer)
            await self.startRoom.Enter(self.currentPlayer)


        else:
            minPlayers = ("\n" + "minmum amount of players is " + str(self.minParty)) if self.minParty > 0 else ""
            maxPlayers = ("\n" + "maximum amount of players is " + str(self.maxParty)) if self.maxParty > 0 else ""
            raise Exception("The Party is not sized for this adventure." + minPlayers + maxPlayers)

    def RemoveCommandByName(self, commandName : str) -> None:
        for c in self.commands:
            if commandName in c.aliases + c:
                self.commands.remove(c)
                return

    async def ExecuteCommand(self, command : str, executioner : Player.Player, message : str) -> bool:

        for c in self.commands:
            commandNames = c.aliases + [c.name]
            if command in commandNames:
                return await c(executioner, message)

    async def ToggleVoice(self, voiceChannel : discord.VoiceChannel) -> None:

        self.useVoice = not self.useVoice
        if self.useVoice:
            voiceClient = await voiceChannel.connect()
            GlobalVars.botVoiceClients[voiceChannel.guild.id] = voiceClient

            if self.playingBackgroundMusic:
                self.ResumeBackgroundMusic()

        else:
            voiceClient = GlobalVars.botVoiceClients[voiceChannel.guild.id]
            await voiceClient.disconnect()
            GlobalVars.botVoiceClients.pop(voiceChannel.guild.id)

    def GetRoomByName(self, name : str) -> Room:
        for r in self.rooms:
            if r.name == name:
                return r

    def Reset(self) -> None:
        self.party = None

    def SetBackgroundMusic(self, trackName : str) -> None:
        self.backgroundTrack = trackName
        self.playingBackgroundMusic = True
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[self.channel.guild.id]
            if voiceClient.is_playing():
                voiceClient.stop()
            voiceClient.play(discord.FFmpegPCMAudio(trackName))

    def PauseBackgroundMusic(self) -> None:
        self.playingBackgroundMusic = False
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[self.channel.guild.id]
            voiceClient.stop()

    def ResumeBackgroundMusic(self) -> None:
        self.playingBackgroundMusic = True
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[self.channel.guild.id]
            voiceClient.play(discord.FFmpegPCMAudio(self.backgroundTrack))

    def StopBackgroundMusic(self) -> None:
        self.backgroundTrack = ""
        self.playingBackgroundMusic = False
        if self.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[self.channel.guild.id]
            voiceClient.stop()

    def End(self) -> None:

        for p in self.party:
            p.character.room = None

    def command(self, aliases : List[str] = []):

        def decorator(foo : Callable[[Player.Player, str], Awaitable[bool]]):

            cmd = Command(foo.__name__, foo.__doc__, foo, aliases)
            self.commands.append(cmd)

        return decorator
