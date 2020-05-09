from Action import Action
from typing import *
import Sequence

class Room:

    def __init__(self, name, description : Sequence.Sequence, shortDescription : Sequence.Sequence, **DunderActions):

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
        EmptyAction = Action('', '', empty, room=self)

        self.onEnter : Action = DunderActions.get('onEnter', EmptyAction)
        self.onLeave : Action = DunderActions.get('onLeave', EmptyAction)

    def AddAction(self, action : Action, index = None):
        if index == None:
            self.actions.append(action)
        else:
            self.actions.insert(index, action)

    async def Enter(self, ctx, players):

        self.players.extend(players)
        for player in players:
            player.character.room = self

        if not self.entered:
            self.entered = True
            await self.description.Play(ctx.channel)
        else:
            await self.shortDescription.Play(ctx.channel)

        actionsStr = "possible actions:\n"
        for i in range(len(self.actions)):
            a = self.actions[i]
            spacesToDescription = 8
            actionsStr += f"{i + 1}. {a.name}{(spacesToDescription * ' - ' + a.description) if a.description != None and a.description != '' else ''}" + "\n"
        await ctx.send(actionsStr)


        await self.onEnter(ctx, players)

    async def Leave(self, players, ctx):

        for p in players:
            self.players.remove(p)
            p.room = None

        self.left = True

        await self.onLeave(ctx, players)

    def action(self, *, condition: Callable[[], bool] = lambda: True, index=-1, failFeedback="the action cant be executed, something is missing."):

        def decorator(function):
            actionObj = Action(
                CapStrToSpaced(function.__name__),
                function.__doc__,
                function,
                condition,
                self,
                failFeedback
            )

            self.AddAction(actionObj, index)
            return actionObj

        return decorator


def CapStrToSpaced(string : str):

    #newStr starts with a colon to allow to index it.
    #wil be replaced in return.
    newStr = ":"

    for i in range(len(string)):
        l = string[i]
        if newStr[-1] == " ":
            newStr += l.lower()
        else:
            if l.isupper() or l.isnumeric():
                newStr += " " + l.lower() if i != 0 else l.lower()
            elif l == '_' or l == '-':
                newStr += " "
            else:
                newStr += l

    return newStr[1:]


