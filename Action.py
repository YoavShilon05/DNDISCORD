from typing import *
import Player
import discord
import Functions
from inspect import getfullargspec

class Condition():

    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def __call__(self):
        args = getfullargspec(self.condition).args

        if len(args) == 0:
            return self.condition()
        elif len(args) == 1:
            return self.condition(self.action)

class Action:

    def __init__(self, name : str, description : str, action : Callable, passTurn=False):
        self.name = name
        self.description = description
        self.action = action
        self.condition = Condition(lambda : True, self)
        self.passTurn = passTurn
        self.room = None


    async def __call__(self, channel : discord.TextChannel, executioner : Player.Player, message=None):

        if self.condition():
            await Functions.CallAction(self.action, channel, executioner, None)
            return self.passTurn
        else:
            return True

    def Condition(self, function):
        self.condition.condition = function

