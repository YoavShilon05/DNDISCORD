from typing import List

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
            raise Exception("party leader not in party.")