from typing import *
from Player import Player
from inspect import getfullargspec
import discord
from Functions import CallAction


class Action:

    def __init__(self, name : str, description : str, action : Callable, condition : Callable[[], bool] = lambda : True, passTurn=True, failFeedback="the action cant be executed, something is missing."):
        self.name = name
        self.description = description
        self.action = action
        self.condition = condition
        self.passTurn = passTurn
        self.room = None
        self.failFeedback = failFeedback


    async def __call__(self, message : discord.Message, executioner : Player):

        if self.condition():
            await CallAction(self.action, message, executioner)
            return not self.passTurn
        else:
            await message.channel.send(self.failFeedback)
            return False


