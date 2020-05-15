from __future__ import annotations
from typing import *
import discord
import random

if TYPE_CHECKING:
    from Room import Room

class Player:

    def __init__(self, author):

        self.author : discord.Member = author
        self.nickname = author.name
        self.characters = []
        self.character = None
        self.adventure = None
        self.adventuresPlayed = set()

        self.party : Party = Party([self])

    def AddCharacter(self, character):
        self.characters.append(character)

    def Enter(self, ctx,  room : Room):
        room.Enter(ctx, [self])

    def SetNickname(self, newNickname):
        self.nickname = newNickname

    def SetAdventure(self, adventure):
        self.adventure = adventure

    def Reset(self):
        self.party = None
        self.adventure = None

    def SetCharacter(self, character):
        if character in self.characters:
            self.character = character
        else:
            raise Exception(f"character {character.name} is not in {self.author.name}'s character bank.")


class Party:
    def __init__(self, players):
        self.players : List[Player] = players
        self.partyLeader : Player or None = None
        self.partyLeader = random.choice(self.players)

    def AddPlayer(self, player : Player):
        self.players.append(player)
        player.party = self

    def SetPartyLeader(self, player):
        if player in self.players:
            self.partyLeader = player
        else:
            raise Exception("party leader not in party")

    def Kick(self, player : Player):
        self.players.remove(player)
        player.party = Party([player])
        if self.partyLeader == player:
            self.partyLeader = self.players[0]

    def __getitem__(self, item) -> Player:

        if type(item) == discord.Member or type(item) == discord.User:

            for p in self.players:
                if p.author == item:
                    return p
            raise KeyError(f"player {item} not in party")

        elif type(item) == int:
            return self.players[item]

        else:
            raise TypeError(f"party object can't index {type(item)} object")

    def __len__(self):
        return len(self.players)