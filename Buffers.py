from typing import List
import Races

class Buffer:

    def __init__(self, name, damage, duration, description=""):
        self.name = name
        self.damage = damage
        self.description = description
        self.duration = duration


class RaceBuffer(Buffer):

    def __init__(self, name, damage, races : List[Races.Races], description=""):

        super().__init__(name, damage, description)

        self.races = races
