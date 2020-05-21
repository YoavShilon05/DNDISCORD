
import Item
import Weapon
import Character
from typing import *


class Inventory():

    def __init__(self, owner : Character.Character, weaponSlots : int, itemSlots : int) -> None:
        self.owner : Character.Character = owner
        self.weaponSlots : int = weaponSlots
        self.itemSlots : int = itemSlots

        self.items : List[Item.Item] = []
        self.weapons = []

    def Preview(self) -> str:
        spaces = 8
        return '\n'.join([i.name + " - " * spaces + i.description for i in self.items])

    async def UseItem(self, ctx, user, item : Item.Usable):

        if item in self.items:
            await item.Use(ctx, user)

            item.uses -= 1

            if item.uses == 0:
                self.items.remove(item)
                del item

    def AddItem(self, item : Item):

        if type(item) == Weapon.Weapon:
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
        self.owner.room.AddItem(item)

    def RemoveItem(self, item):
        if type(item) == Weapon:
            if len(self.weapons) < self.weaponSlots:
                self.weapons.remove(item)
        else:
            if len(self.items) < self.itemSlots:
                self.items.remove(item)



    def __getitem__(self, item : int):
        inv = self.weapons.extend(self.items)
        return inv[item]
