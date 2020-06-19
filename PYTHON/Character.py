
"""
this file contains classes that the charcter is built out of.
"""

from __future__ import annotations
import enum
import Adventure
from typing import *
import Player
from itertools import cycle
import GlobalVars
import discord

class PersonalityPoints(enum.Enum):

    strength = 0
    intelligence = 1
    charisma = 2
    agility = 3
    defense = 4
    sustainability = 5

def MakePersonalityPoints(defaultValue=1, **personalityPoints : float) -> Dict[PersonalityPoints, float]:

    result : Dict[PersonalityPoints, float] = {}
    for p in PersonalityPoints:
        result[p] = personalityPoints.get(p, defaultValue)

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
    goblin = MakePersonalityPoints()
    dobgoblin = MakePersonalityPoints()
    skeleton = MakePersonalityPoints()
    zombie = MakePersonalityPoints()
    creeper = MakePersonalityPoints()
    yeti = MakePersonalityPoints()
    ape = MakePersonalityPoints()
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
    none = MakePersonalityPoints()
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


defaultPersonalityPoints = MakePersonalityPoints()


class Character:
    def __init__(self, name, sex : Sexes, race : Races, profession : Professions, backstory="",
                 personalityPoints : Dict[PersonalityPoints, float] = MakePersonalityPoints()):
        self.name : str = name
        self.sex : Sexes = sex
        self.race : Races = race
        self.profession : Professions = profession

        self.personalityPoints : Dict[PersonalityPoints, float] = personalityPoints
        for p in PersonalityPoints:
            self.personalityPoints[p] = self.profession.value[p] + self.race.value[p]

        self.maxHealth : float = defaultPersonalityPoints[PersonalityPoints.sustainability] + \
                                 self.personalityPoints[PersonalityPoints.sustainability]
        self._health : float = self.maxHealth
        self.damage : float = defaultPersonalityPoints[PersonalityPoints.strength] + \
                              self.personalityPoints[PersonalityPoints.strength]
        self.armor : float = defaultPersonalityPoints[PersonalityPoints.defense] + \
                             self.personalityPoints[PersonalityPoints.defense]

        self.backstory : str = backstory
        self.inventory : Inventory = Inventory(self, 2, 7)
        self.mainWeapon : Weapon = None
        self.room : Adventure.Room = None
        self.player = None

        self.currency : int = 0

        async def empty(executioner : Player.Player, amount : float):
            pass

        self.onDamageTaken : Callable[[Player.Player, float], Awaitable[None]] = empty
        self.onHealingTaken : Callable[[Player.Player, float], Awaitable[None]] = empty
        self.onDeath : Callable[[Player.Player, float], Awaitable[None]] = empty

        self.health = property(self._HealthGetter, self._HealthSetter)
        self.dead : bool = False

        self.buffers : List[WeaponBuffer] = []

    def _HealthSetter(self, amount : float):
        #set health
        self._health += amount
        if self._health > self.maxHealth:
            self._health = self.maxHealth

        if self._health <= 0:
            self.Kill()

    def _HealthGetter(self):
        return self._health

    def Kill(self):
        self.dead = True

    async def Attack(self, enemy) -> float:
        fists = Weapon("", "", self.damage, 0)
        fists.buffers = self.buffers

        if self.mainWeapon != None:
            return await self.mainWeapon.Attack(enemy) + await fists.Attack(enemy)
        else:
            return await fists.Attack(enemy)

    def Possess(self, player):
        self.player = player

class Inventory:

    def __init__(self, owner : Character, weaponSlots : int, itemSlots : int) -> None:
        self.owner : Character = owner
        self.weaponSlots : int = weaponSlots
        self.itemSlots : int = itemSlots

        self.items : List[Item] = []
        self.weapons = []

    def Preview(self) -> str:
        spaces = 8
        return '\n'.join([i.name + " - " * spaces + i.description for i in self.items])

    async def UseItem(self, item : Usable):

        if item in self.items:
            await item.Use()

            item.uses -= 1

            if item.uses == 0:
                self.items.remove(item)
                del item

    def AddItem(self, item : Item):

        if type(item) == Weapon:
            if len(self.weapons) < self.weaponSlots:
                self.weapons.append(item)
                return
        else:
            if len(self.items) < self.itemSlots:
                self.items.append(item)
                return

        raise IndexError("item does not fit in inventory")

    def DropItem(self, item):
        self.RemoveItem(item)
        self.owner.room.items.append(item)

    def RemoveItem(self, item):
        if type(item) == Weapon:
            if len(self.weapons) < self.weaponSlots:
                self.weapons.remove(item)
        else:
            if len(self.items) < self.itemSlots:
                self.items.remove(item)

    def __getitem__(self, item : int):
        inv = self.weapons.copy().extend(self.items.copy())
        return inv[item]



class Item:
    def __init__(self, name, description, fullDescription=None):
        self.inventory = None
        self.name = name

        self.description = description
        self.fullDescription = fullDescription

    def Preview(self):
        spaces = 8

        return self.name + spaces * " - " + self.fullDescription

    def __str__(self):
        return self.Preview()

    def __repr__(self):
        return self.Preview()

class WeaponBuffer:

    def __init__(self, boost, sexBoosts : Dict[Sexes, float] = {}, raceBoosts : Dict[Races, float] = {},
                 professionBoosts : Dict[Professions, float] = {}):
        self.boost : float = boost
        self.sexBoosts : Dict[Sexes, float] = sexBoosts
        self.raceBoosts : Dict[Races, float] = raceBoosts
        self.professionBoosts : Dict[Professions, float] = professionBoosts

    def GetBoost(self, enemy : Character):

        boost = self.boost

        if enemy.sex in self.sexBoosts.keys():
            boost += self.sexBoosts[enemy.sex]
        if enemy.race in self.raceBoosts.keys():
            boost += self.raceBoosts[enemy.race]
        if enemy.sex in self.professionBoosts.keys():
            boost += self.professionBoosts[enemy.profession]

        return boost


class Usable(Item):

    def __init__(self, name, description, useFunc : Callable[[Player.Player], Awaitable[bool]], uses: int=1, fullDescription=None):

        super().__init__(name, description, fullDescription)

        self.useFunc = useFunc
        self.uses = uses

    async def Use(self):

        await self.useFunc(self.inventory.owner)
        self.uses -= 1

        if self.uses <= 0:
            self.inventory.RemoveItem(self)

class Weapon(Item):

    def __init__(self, name, description, damage, durability):

        super().__init__(name, description)

        self.damage : float = damage
        self.durability : int = durability
        self.buffers : List[WeaponBuffer] = []

    async def Attack(self, enemy : Character) -> float:

        if self.durability > 0:
            self.durability -= 1

            if self.durability == 0:
                if self.inventory != None:
                    self.inventory.RemoveItem(self)

        damage = self.damage
        damage += sum([b.GetBoost(enemy) for b in self.buffers])

        #trigger events

        if self.inventory != None:
            if damage > 0:
                await enemy.onHealingTaken(self.inventory.owner, damage)
            elif damage < 0:
                await enemy.onDamageTaken(self.inventory.owner, damage)
                if enemy.health - damage <= 0:
                    await enemy.onDeath(self.inventory.owner, damage)


        enemy.health -= damage / enemy.armor

        return damage


