import Inventory
import enum
import Room

class Sexes(enum.Enum):
    male = 0
    female = 1
    unknown = 2


import enum

class Races(enum.Enum):
    # first item in list specifies level (0, good / hero, 1 - passive, 2 - hostile, 3 - boss)
    # second item in list specifies index.
    #good / heroes
    Elf = [0, 0]
    Dwarf = [0, 1]
    Halfling = [0, 2]
    Halfelf = [0, 3]

    #passive
    Human = [1, 4]
    Dragonborn = [1, 5]
    Halforc = [1, 6]
    Goliath = [1, 7]
    Triton = [1, 8]

    #hostile
    Goblins = [2, 9]
    Dobgoblins = [2, 10]
    Skeletons = [2, 11]
    Zombies = [2, 12]
    Creepers = [2, 13]
    Yeti = [2, 14]
    Apes = [2, 15]
    Darkelf = [2, 16]

    #Bosses
    Beholder = [3, 17]
    Dragon = [3, 18]
    Pheonix = [3, 19]
    Gelatinous_cube = [3, 20]
    Orc = [3, 21]
    #black_dragon = 3
    #blue_dragon = 3
    #brass_dragon = 3
    #bronze_dragon = 3
    #copper_dragon = 3
    #gold_dragon = 3
    #green_dragon = 3
    #red_dragon = 3
    #silver_dragon = 3

class Profession():
    def __init__(self, name, personalityPointBuffs):
        self.name = name
        self.personalityPointBuffs = personalityPointBuffs

class PersonalityPoints(enum.Enum):

    strength = 0
    intelligence = 1
    charisma = 2
    agility = 3
    defense = 4

def MakePersonalityPoints(**personalityPoints):

    result = {}
    for p in PersonalityPoints:
        result[p.name] = personalityPoints.get(p, 0)

    return result

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

class Entity:
    def __init__(self, name, sex : Sexes, race, backstory=""):
        self.name = name
        self.sex = sex

        self.race = race

        #TODO: make health & dmage be affected by races & profession.
        self.maxHealth = 25
        self._health = 5
        self.damage = 15

        self.backstory = backstory
        self.inventory = Inventory.Inventory(self, 2, 7)
        self.mainWeapon = None
        self.room: Room.Room = None

    #Health doesnt go above max
    def _HealthGetter(self):
        return self._health

    def _HealthSetter(self, val):
        if self._health + val > self.maxHealth:
            self._health = self.maxHealth
            print("Health was set to over max, set it back to max.")
        else:
            self._health += val

    health = property(_HealthGetter, _HealthSetter)

    async def Attack(self):
        pass

class Character(Entity):

    def __init__(self, name, sex, race, profession, backstory=""):
        super().__init__(name, sex, race, backstory)

        self.race = race
        self.profession = profession

