from typing import *
from Player import Player
from inspect import getfullargspec




class Action:

    def __init__(self, name : str, description : str, action : Callable, condition : Callable[[], bool] = lambda : True, room=None,**properties):
        self.name = name
        self.description = description if description != None and description != "" else name
        self.action = action
        self.condition = condition
        self.room = room

    async def __call__(self, *args):



        if self.condition():
            if len(getfullargspec(self.action).args) == 0:
                await self.action()
            elif len(getfullargspec(self.action).args) == 1:
                context = args[0]
                await self.action(context)
            elif len(getfullargspec(self.action).args) == 2:
                context = args[0]
                executioners = args[1]
                await self.action(context, executioners)
        else:
            raise Exception("Condition was false.")


