from __future__ import annotations
from typing import TYPE_CHECKING
from inspect import iscoroutinefunction, getfullargspec
from uuid import uuid1

if TYPE_CHECKING:
    from Inventory import Inventory


class Item:
    def __init__(self, name, inventory : Inventory, **properties):
        self.inventory = inventory
        self.name = name

        self.id = uuid1()

        self.shortDescription = properties.get("description", "no description provided")
        self.longDescription = properties.get("longDescription", self.shortDescription)


class Usable(Item):

    def __init__(self, name, inventory: Inventory, useFunction, uses: int=1, **properties):
        if iscoroutinefunction(useFunction):
            # if num of args of function are or more then 2 (ctx, user)
            if len(getfullargspec(self.useFunction).args) >= 2:
                self.useFunction = useFunction
            else:
                raise TypeError("Expected 2 Attributes in use function, 1 was given")

        else:
            raise Exception("use function is not coroutine")

        super().__init__(name, inventory, **properties)

        self.uses = uses

    async def Use(self, ctx, user):
        await self.useFunction(ctx, user)



