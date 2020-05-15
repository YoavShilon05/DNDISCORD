import Action
from typing import *
import Sequence
import Functions
import functools

class Room:

    def __init__(self, name, description : Sequence.Sequence, shortDescription : Sequence.Sequence):

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

        async def empty():
            print("empty function called")
        EmptyAction = Action.Action('', '', empty)

        self.onEnter : Action.Action = EmptyAction
        self.onLeave : Action.Action = EmptyAction

    def AddAction(self, action : Action.Action, index = None):
        if index == None:
            self.actions.append(action)
        else:
            self.actions.insert(index, action)
        return action

    async def Enter(self, channel, player):

        self.players.append(player)
        if player.character.room != None:
            await player.character.room.Leave(channel, player)

        player.character.room = self
        await self.onEnter(channel, player)

        if not self.entered:
            self.entered = True
            await self.description.Play(channel)
        else:
            await self.shortDescription.Play(channel)

        actionsStr = "possible actions:\n"
        for i in range(len(self.actions)):
            a = self.actions[i]
            spacesToDescription = 8
            actionsStr += f"{i + 1}. {a.name}{(spacesToDescription * ' - ' + a.description) if a.description != None and a.description != '' else ''}" + "\n"
        await channel.send(actionsStr)


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

    def action(self, *, condition: Callable[[], bool] = lambda: True, index=-1, passTurn=False,
               rooms=[], failFeedback="the action cant be executed, something is missing."):

        def decorator(function):
            actionObj = Action.Action(
                Functions.SpaceFunctionName(function.__name__),
                function.__doc__,
                function,
                condition,
                passTurn,
                failFeedback
            )

            rooms.append(self)
            for r in rooms:
                if actionObj.name == "on enter":
                    r.onEnter = actionObj
                elif actionObj.name == "on leave":
                    r.onLeave = actionObj
                else:
                    r.AddAction(actionObj, index)
                return actionObj

        return decorator
