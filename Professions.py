import enum
from PersonalityPoints import MakePersonalityPoints

class Profession():
    def __init__(self, name, personalityPointBuffs):
        self.name = name
        self.personalityPointBuffs = personalityPointBuffs

class Professions(enum.Enum):
    Thief = MakePersonalityPoints(damage=12, health=13)
    Knight = 1
    Barbarian = 0
    Archer = 2
    Warrior = 3
    Druid = 4
    Wizard = 5
    Monk = 6
    Warlock = 7
    Sorcerer = 8
    Cleric = 9
