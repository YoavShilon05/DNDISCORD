from __future__ import annotations
import Inventory
import enum
import Room
import Weapon
from typing import *

class PersonalityPoints(enum.Enum):

    strength = 0
    intelligence = 1
    charisma = 2
    agility = 3
    defense = 4
    sustainability = 5

def MakePersonalityPoints(**personalityPoints : int):

    result : Dict[str, int] = {}
    for p in PersonalityPoints:
        result[p.name] = personalityPoints.get(p, 0)

    return result


class Sexes(enum.Enum):
    male = 0
    female = 1
    unknown = 2

class Races(enum.Enum):
    # first item in list specifies level (0, good / hero, 1 - passive, 2 - hostile, 3 - boss)
    # second item in list specifies index.
    #good / heroes
    elf = MakePersonalityPoints()
    dwarf = MakePersonalityPoints()
    halfling = MakePersonalityPoints()
    halfelf = MakePersonalityPoints()

    #passive
    human = MakePersonalityPoints()
    dragonborn = MakePersonalityPoints()
    halforc = MakePersonalityPoints()
    goliath = MakePersonalityPoints()
    triton = MakePersonalityPoints()

    #hostile
    goblins = MakePersonalityPoints()
    dobgoblins = MakePersonalityPoints()
    skeletons = MakePersonalityPoints()
    zombies = MakePersonalityPoints()
    creepers = MakePersonalityPoints()
    yeti = MakePersonalityPoints()
    apes = MakePersonalityPoints()
    darkelf = MakePersonalityPoints()

    #Bosses
    beholder = MakePersonalityPoints()
    dragon = MakePersonalityPoints()
    pheonix = MakePersonalityPoints()
    gelatinous_cube = MakePersonalityPoints()
    orc = MakePersonalityPoints()
    #black_dragon = 3
    #blue_dragon = 3
    #brass_dragon = 3
    #bronze_dragon = 3
    #copper_dragon = 3
    #gold_dragon = 3
    #green_dragon = 3
    #red_dragon = 3
    #silver_dragon = 3

class Professions(enum.Enum):
    thief = MakePersonalityPoints(damage=12, health=13)
    knight = MakePersonalityPoints()
    barbarian = MakePersonalityPoints()
    archer = MakePersonalityPoints()
    warrior = MakePersonalityPoints()
    druid = MakePersonalityPoints()
    wizard = MakePersonalityPoints()
    monk = MakePersonalityPoints()
    warlock = MakePersonalityPoints()
    sorcerer = MakePersonalityPoints()
    cleric = MakePersonalityPoints()


defaultPersonalityPoints = MakePersonalityPoints(sustainability=25, strength=15)





class Entity:
    def __init__(self, name, sex : Sexes, race : Races, profession : Professions, backstory="") -> None:
        self.name : str = name
        self.sex : Sexes = sex
        self.race : Races = race
        self.profession : Professions = profession

        self.personalityPoints : dict = {}
        for p in PersonalityPoints:
            self.personalityPoints[p.name] = self.profession.value[p.name] + self.race.value[p.name]

        self.maxHealth : int = defaultPersonalityPoints['sustainability'] + self.personalityPoints['sustainability']
        self.health : int = self.maxHealth
        self.damage : int = defaultPersonalityPoints['strength'] + self.personalityPoints['strength']

        self.backstory : str = backstory
        self.inventory : Inventory.Inventory = Inventory.Inventory(self, 2, 7)
        self.mainWeapon : Weapon.Weapon = None
        self.room: Room.Room = None

        self.currency : int = 0

    def Attack(self, enemy : Entity) -> int:
        pass

    def AddCurrency(self, amount : int) -> int:
        self.currency += amount if self.currency + amount >= 0 else 0
        return self.currency

    def AddHealth(self, amount : int) -> int:
        if self.health + amount >= 0:
            if self.health + amount <= self.maxHealth:
                self.health += amount if self.health + amount >= 0 else 0
            else:
                self.health = self.maxHealth
        return self.health

class Character(Entity):
    pass
