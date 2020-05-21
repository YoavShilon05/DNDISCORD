import Action
from typing import *
import Sequence
import Functions
import Item
import asyncio


class Room:

    def __init__(self, name, description : Sequence.Sequence, shortDescription : Sequence.Sequence, items : List[Item.Item] = []):

        self.name = name
        self.description : Sequence.Sequence = description
        self.description.room = self
        self.shortDescription : Sequence.Sequence = shortDescription
        self.shortDescription.room = self
        self.actions : List[Action] = []

        self.adventure = None
        self.players = []
        self.entered = False
        self.left = False
        self.numberedActions = self.actions.copy()
        self.UpdateNumberedActions()

        async def empty():
            print("empty function called")
        EmptyAction = Action.Action('', '', empty)

        self.onEnter : Action.Action = EmptyAction
        self.onLeave : Action.Action = EmptyAction

        self._itemActions = []
        self.items = []

        #if not shop
        if type(self) != Shop:
            for i in items:
                self.AddItem(i)

    def AddAction(self, action : Action.Action, index = None):
        if index == None:
            self.actions.append(action)
        else:
            self.actions.insert(index, action)
        self.UpdateNumberedActions()
        return action

    def UpdateNumberedActions(self):
        self.numberedActions.clear()
        falseActions = []
        itemActions = []
        for a in self.actions:
            if a.condition():
                if a in self._itemActions:
                    itemActions.append(a)
                else:
                    self.numberedActions.append(a)
            else:
                falseActions.append(a)
        self.numberedActions.extend(itemActions)
        self.numberedActions.extend(falseActions)

    def AddItem(self, item):
        async def TakeItem(channel, player):
            try:
                player.character.room.RemoveItemByName(item.name)
                player.character.inventory.AddItem(item)
                await channel.send(f"{player.character.name} has taken the {item.name}")
                await asyncio.sleep(1)
                await channel.send(player.character.room.GetActionRepr())
            except IndexError:
                await channel.send("Your inventory is full. You can not carry this item.")

        action = Action.Action(item.name.lower(), item.description, TakeItem)

        self.items.append(item)
        self.AddAction(action)
        self._itemActions.append(action)

    def RemoveItemByName(self, item):
        for a in self._itemActions:
            if a.name == item:
                self._itemActions.remove(a)
                self.actions.remove(a)

    def RemoveAction(self, action):
        self.actions.remove(action)

        if action in self._itemActions:
            self._itemActions.remove(action)

    async def Enter(self, channel, player):

        self.players.append(player)
        if player.character.room != None:
            await player.character.room.Leave(channel, player)

        player.character.room = self
        await self.onEnter(channel, player, "")

        if not self.entered:
            self.entered = True
            await self.description.Play(channel)
        else:
            await self.shortDescription.Play(channel)

        self.UpdateNumberedActions()

        await channel.send(self.GetActionRepr())

    def SilentEnter(self, player):
        if player.character.room != None:
            player.room.SilentLeave(player)
        self.players.append(player)
        player.character.room = self

    async def Leave(self, channel, player):
        self.players.remove(player)
        player.character.room = None

        self.left = True

        await self.onLeave(channel, player)

    def SilentLeave(self, player):
        self.players.remove(player)
        player.character.room = None

    def action(self, *, condition: Callable[[], bool] = lambda: True, index=-1, passTurn=False, rooms=[]):

        def decorator(function):
            actionObj = Action.Action(
                Functions.SpaceFunctionName(function.__name__),
                function.__doc__,
                function,
                passTurn
            )
            actionObj.Condition(condition)
            actionObj.room = self
            rooms.append(self)

            for r in rooms:
                if actionObj.name == "on enter":
                    r.onEnter = actionObj
                elif actionObj.name == "on leave":
                    r.onLeave = actionObj
                else:
                    r.AddAction(actionObj, index)
                return actionObj

            self.UpdateNumberedActions()

        return decorator

    def GetActionByName(self, name) -> Action.Action:

        for a in self.actions:
            if a.name == Functions.SpaceFunctionName(name):
                return a

    def GetActionRepr(self):
        self.UpdateNumberedActions()

        actionsStr = ""

        if len(self.actions) - len(self._itemActions) > 0:
            actionsStr = 'possible actions:\n'

            spacesToDescription = 8
            for i in range(len(self.numberedActions)):
                a = self.numberedActions[i]
                if a.condition():
                    if a not in self._itemActions:
                        actionsStr += f"{i + 1}. {a.name}{(spacesToDescription * ' - ' + a.description) if a.description != None and a.description != '' else ''}" + "\n"

                # numbered actions are arranged so false actions are at the end, we can break once we get to a false one.
                else:
                    break

        if len(self._itemActions) > 0:
            actionsStr += "items:\n"

            for i in self.items:
                actionsStr += i.name + "\n"

        return actionsStr

    def GetItemByName(self, item):

        for i in self.items:
            if i.name == item:
                return i

    def RemoveItem(self, item):
        self.items.remove(item)
        self.RemoveAction(self._GetItemActionByItem(item))

    def _GetItemActionByItem(self, item):

        itemIndex = self.items.index(item)
        return self._itemActions[itemIndex]


class Shop(Room):

    def __init__(self, name, description : Sequence.Sequence, room, items : List[Tuple[Item.Item, int, int]]):
        self.itemsOnOffer = items.copy()

        # room init does not support shop item handling.
        super().__init__(name, description, description, [])

        # shop item handler

        for i in items:
            self.AddItem(i[0], i[1], i[2])

        Functions.ConnectRooms(room, self)

    def GetActionRepr(self):

        spaces = 8
        actionStr = "Shop:\n"
        for a in self.itemsOnOffer:
            actionStr += str(a[2]) + " " + a[0].name + spaces * " - " + str(a[1]) + "$"

    def AddItem(self, item, price, stock):

        self.itemsOnOffer.append((item, price, stock))
        self.items.append(item)

        async def BuyItem(channel, player):
            if player.character.currency >= price:
                await channel.send(f"{player.character.name} has bought {'a' if item.name[0].islower() else 'an'} {item.name}")
                player.character.inventory.AddItem(item)
                # decrease the stock of the item by one

                itemOnStock = self.GetItemOnStockByName(item.name)
                itemOnStock[2] -= 1
                if itemOnStock[2] <= 0:
                    self.RemoveItem(item)

        action = Action.Action(item.name.lower(), item.description, BuyItem)

        self.AddAction(action)
        self._itemActions.append(action)

    def GetItemOnStockByName(self, name):
        for a in self.itemsOnOffer:
            if a[0].name == name:
                return a
        raise IndexError("item not found")