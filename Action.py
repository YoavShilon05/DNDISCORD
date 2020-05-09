from typing import *
from Player import Player
from inspect import getfullargspec




class Action:

    def __init__(self, name : str, description : str, action : Callable, condition : Callable[[], bool] = lambda : True, room=None, failFeedback="the action cant be executed, something is missing."):
        self.name = name
        self.description = description
        self.action = action
        self.condition = condition
        self.room = room
        self.failFeedback = failFeedback

    async def __call__(self, ctx, executioner : Player):



        if self.condition():
            if len(getfullargspec(self.action).args) == 0:
                await self.action()
            elif len(getfullargspec(self.action).args) == 1:
                await self.action(ctx)
            elif len(getfullargspec(self.action).args) == 2:
                await self.action(ctx, executioner)
        else:
            await ctx.send(self.failFeedback)


