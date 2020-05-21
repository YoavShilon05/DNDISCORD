from uuid import uuid1
import Functions


class Item:
    def __init__(self, name, description, fullDescription=None):
        self.inventory = None
        self.name = name

        self.id = uuid1()

        self.description = description
        self.fullDescription = fullDescription

    def Preview(self):
        spaces = 8

        return self.name + spaces * " - " + self.fullDescription

class Usable(Item):

    def __init__(self, name, description, useFunc, uses: int=1, fullDescription=None):

        super().__init__(name, description, fullDescription)

        self.useFunc = useFunc
        self.uses = uses

    async def Use(self, channel, user):

        await Functions.CallAction(self.useFunc, channel, user, None)
        self.uses -= 1

        if self.uses <= 0:
            self.inventory.RemoveItem(self)



