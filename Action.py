from typing import *
from Player import Player
from discord.ext.commands import Context

class Action:

    def __init__(self, name : str, description : str, action : Callable[[Player, Context], None], condition : Callable[[], None], **properties):
        self.name = name
        self.description = description
        self.action = action
        self.condition = condition

    def Execute(self, executioner : Player, context : Context):
        self.action(executioner, context)


