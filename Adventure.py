from typing import *
from Room import Room

class Adventure:

    def __init__(self, name, description, rooms : List[Room], startRoom : Room):

        self.name = name
        self.description = description
        self.rooms = rooms
        self.startRoom = startRoom

        self.players = []


    def Init(self, players):

        for p in players:
            self.startRoom.Enter()