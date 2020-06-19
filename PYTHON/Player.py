
"""this file contains classes that have to do with the Player object"""

from __future__ import annotations
from typing import *
import discord
import random
import Character

import Adventure

class Player:

    """
    contains info and methods on the player, his history, and current data.
    """

    def __init__(self, author : discord.Member):

        self.author : discord.Member = author
        self.nickname : str = author.name
        self.characters : List[Character.Character] = []
        self.character : Character.Character = None
        self.adventure : Adventure.Adventure = None
        self.adventuresPlayed : Set[Adventure.Adventure] = set()

        self.party : Party = Party([self])

    def Reset(self):
        self.party = None
        self.adventure = None

        for c in self.characters:
            c.player = None


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