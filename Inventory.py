
from Item import Item, Usable
from Weapon import Weapon
from typing import *


class Inventory():

    def __init__(self, owner, weaponSlots : int, itemSlots : int):
        super().__init__()
        self.owner = owner
        self.weaponSlots = weaponSlots
        self.itemSlots = itemSlots

        self.weapons = List[Weapon]
        self.items = List[Item]
        self.weapons = []
        self.items = []

    def Preview(self):
        spaces = 8
        return '\n'.join([i.name + " - " * spaces + i.description for i in self.items])

    async def UseItem(self, ctx, user, item : Usable):

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

