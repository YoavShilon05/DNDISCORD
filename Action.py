from typing import *
from Player import Player
from discord.ext.commands import Context

class Action:

    def __init__(self, name : str, description : str, action : Callable[[Player, Context], None], condition : Callable[[], bool], **properties):
        self.name = name
        self.description = description
        self.action = action
        self.condition = condition

    def Execute(self, executioner : Player, context : Context):

        if self.condition():
            self.action(executioner, context)
        else:
            raise Exception("Condition was false.")

