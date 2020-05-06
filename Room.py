from Action import Action, ExecuteAction
from Player import Party
from typing import List
from inspect import getfullargspec


class Room:

    def __init__(self, name, description, shortDescription, actions : List[Action], **DunderActions):

        self.name = name
        self.description = description
        self.shortDescription = shortDescription
        self.actions : List[Action] = actions

        self.adventure = None
        self.players = []
        self._entered = False

        self.onInit : Action or None = DunderActions.get('onInit', None)
        self.onEnter : Action or None = DunderActions.get('onEnter', None)
        self.onLeave : Action or None = DunderActions.get('onLeave', None)

        self.onInit()
    async def Enter(self, ctx, players):

        self.players.extend(players)
        for player in players:
            player.room = self

        if not self._entered:
            self._entered = True
            await ctx.send(self.description)
        else:
            await ctx.send(self.shortDescription)

        await ExecuteAction(self.onEnter, ctx, players)



    async def Leave(self, players, ctx):

        for p in players:
            self.players.remove(p)
            p.room = None

        await ExecuteAction(self.onLeave, ctx, players)


