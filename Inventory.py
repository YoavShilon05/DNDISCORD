
import Item
from Weapon import Weapon
from typing import *

"""
class Inventory():

    def __init__(self, owner, weaponSlots : int, itemSlots : int):
        super().__init__()
        self.owner = owner
        self.weaponSlots = weaponSlots
        self.itemSlots = itemSlots

        self.weapons = List[Weapon]
        self.items = List[Item.Item]
        self.weapons = []
        self.items = []

    def Append(self, item : Item.Item) -> None:

        if type(item) == Weapon:
            if len(self.weapons) < self.weaponSlots:
                self.weapons.append(item)
                return

        else:
            if len(self.items) < self.itemSlots:
                self.items.append(item)
                return

        raise Exception("Inventory is full")

    def Preview(self):
        spaces = 8
        return '\n'.join(i.name + " - " * spaces + i.description for i in self.items)

    async def UseItem(self, ctx, user, item : Item.Usable):

        if item in self.items:
            await item.Use(ctx, user)

            item.uses -= 1

            if item.uses == 0:
                self.items.remove(item)
                del item


    def __getitem__(self, index : int):
        inv = self.weapons.extend(self.items)
        return inv[index]

    def __str__(self):
        return self.Preview()
    def __repr__(self):
        return self.Preview()
"""

import Item
from Weapon import Weapon
from typing import *


class Inventory():

    def __init__(self, owner, weaponSlots : int, itemSlots : int):
        super().__init__()
        self.owner = owner
        self.weaponSlots = weaponSlots
        self.itemSlots = itemSlots

        self.weapons = List[Weapon]
        self.items = List[Item.Item]
        self.weapons = []
        self.items = []

    def Append(self, item : Item.Item) -> None:

        if type(item) == Weapon:
            if len(self.weapons) < self.weaponSlots:
                self.weapons.append(item)
                return

        else:
            if len(self.items) < self.itemSlots:
                self.items.append(item)
                return

        raise Exception("Inventory is full")

    def Preview(self):
        spaces = 8
        return '\n'.join(i.name + " - " * spaces + i.description for i in self.items)

    async def UseItem(self, ctx, user, item : Item.Usable):

        if item in self.items:
            await item.Use(ctx, user)

            item.uses -= 1

            if item.uses == 0:
                self.items.remove(item)
                del item

    def __getitem__(self, index : int):
        inv = self.weapons.extend(self.items)
        return inv[index]

    def __str__(self):
        return self.Preview()
    def __repr__(self):
        return self.Preview()

