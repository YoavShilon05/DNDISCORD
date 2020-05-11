from Action import Action
from typing import *
import Sequence
from Functions import SpaceFunctionName

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
        EmptyAction = Action('', '', empty)

        self.onEnter : Action = EmptyAction
        self.onLeave : Action = EmptyAction

    def AddAction(self, action : Action, index = None):
        if index == None:
            self.actions.append(action)
        else:
            self.actions.insert(index, action)
        return action

    async def Enter(self, channel, player):

        self.players.append(player)
        await player.character.room.Leave(channel, player)
        player.character.room = self

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


        await self.onEnter(channel, player)

    async def Leave(self, channel, player):
        self.players.remove(player)
        player.room = None

        self.left = True

        await self.onLeave(channel, player)

    def action(self, *, condition: Callable[[], bool] = lambda: True, index=-1, passTurn, failFeedback="the action cant be executed, something is missing."):

        def decorator(function):
            actionObj = Action(
                SpaceFunctionName(function.__name__),
                function.__doc__,
                function,
                condition,
                failFeedback
            )

            if actionObj.name == "on enter":
                self.onEnter = actionObj
            elif actionObj.name == "on leave":
                self.onLeave = actionObj
            else:
                self.AddAction(actionObj, index)
            return actionObj

        return decorator


