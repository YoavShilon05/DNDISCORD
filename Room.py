from Action import Action
from typing import *


class Room:

    def __init__(self, name, description, shortDescription, **DunderActions):

        self.name = name
        self.description = description
        self.shortDescription = shortDescription
        self.actions : List[Action] = []

        self.adventure = None
        self.players = []
        self.entered = False
        self.left = False

        async def empty(ctx, players):
            print("empty function called")
        EmptyAction = Action('', '', empty, room=self)

        self.onEnter : Action = DunderActions.get('onEnter', EmptyAction)
        self.onLeave : Action = DunderActions.get('onLeave', EmptyAction)

    def AddAction(self, action : Action, index = -1):
        self.actions.insert(index, action)

    async def Enter(self, ctx, players):

        self.players.extend(players)
        for player in players:
            player.character.room = self

        if not self.entered:
            self.entered = True
            await ctx.send(self.description)
        else:
            await ctx.send(self.shortDescription)

        actionsStr = "possible actions:\n"
        for i in range(len(self.actions)):
            a = self.actions[i]
            spacesToDescription = 8
            actionsStr += f"{i + 1}. {a.name}{spacesToDescription * ' - '}{a.description}"
        await ctx.send(actionsStr)


        await self.onEnter(ctx, players)

    async def Leave(self, players, ctx):

        for p in players:
            self.players.remove(p)
            p.room = None

        self.left = True

        await self.onLeave(ctx, players)

    def action(self, *, condition: Callable[[], bool] = lambda: True, index=-1, **properties):

        def decorator(function):
            actionObj = Action(
                CapStrToSpaced(function.__name__),
                function.__doc__,
                function,
                condition,
                self,
                **properties
            )

            self.AddAction(actionObj, index)
            return actionObj

        return decorator


def CapStrToSpaced(string : str):

    newStr = ""

    for i in range(len(string)):
        l = string[i]
        if l.isupper():
            newStr += " " + l.lower() if i != 0 else l.lower()
        elif l == '_' or l == '-':
            newStr += " " if string[i + 1].islower() else ""
        else:
            newStr += l

    return newStr