from typing import List
from discord import Member

class Player:

    def __init__(self, author, nickname):

        self.author = author
        self.nickname = nickname
        self.characters = []
        self.character = None

        self.party : Party or None = None

    def AddCharacter(self, character):
        self.characters.append(character)


class Party:
    def __init__(self):
        self.players : List[Player] = []
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