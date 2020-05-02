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
    Archer = 0
    Warrior = 0
    Druid = 0
    Wizard = 0
    Monk = 0
    Warlock = 0
    Sorcerer = 0
    Cleric = 0

x = Professions.Archer
for i in Professions:
    print(i.name)