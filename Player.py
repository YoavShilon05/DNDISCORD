from __future__ import annotations
from typing import *
from discord import Member

if TYPE_CHECKING:
    from Room import Room

class Player:

    def __init__(self, author):

        self.author = author
        self.nickname = author.name
        self.characters = []
        self.character = None

        self.party : Party or None = None

    def AddCharacter(self, character):
        self.characters.append(character)

    def Enter(self, ctx,  room : Room):
        room.Enter(ctx, [self])

    def SetNickname(self, newNickname):
        self.nickname = newNickname

class Party:
    def __init__(self, players):
        self.players : List[Player] = players
        self.partyLeader : Player or None = None

    def AddPlayer(self, player : Player):
        self.players.append(player)
        player.party = self

    def SetPartyLeader(self, player):
        if player in self.players:
            self.partyLeader = player
        else:
            raise Exception("party leader not in party")

    def __getitem__(self, item):

        if type(item) == Member:

            for p in self.players:
                if p.author == item:
                    return p
            raise KeyError(f"player {item} not in party")

        elif type(item) == int:
            return self.players[item]

        else:
            raise TypeError(f"party object can't index {type(item)} object")