from typing import *
from Player import Player
from discord.ext.commands import Context
from Room import Room
from inspect import getfullargspec





class Action:

    def __init__(self, name : str, description : str, action : Callable, condition : Callable[[], bool], **properties):
        self.name = name
        self.description = description
        self.action = action
        self.condition = condition

    async def Execute(self, *args):

        if self.condition():
            self.action(args)
        else:
            raise Exception("Condition was false.")


async def ExecuteAction(action: Action, context, executioners):
    if len(getfullargspec(action).args) == 0:
        await action.Execute()
    elif len(getfullargspec(action).args) == 1:
        await action.Execute(context)
    elif len(getfullargspec(action).args) == 2:
        await action.Execute(context, executioners)