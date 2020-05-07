
from Item import Item, Usable
from typing import *


class Inventory():

    def __init__(self, owner, weaponSlots : int, itemSlots : int):
        super().__init__()
        self.owner = owner
        self.weaponSlots = weaponSlots
        self.itemSlots = itemSlots

        self.items  = []
        self.weapons = []

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

