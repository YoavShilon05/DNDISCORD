from typing import *
import Player
import discord
import Functions


class Action:

    def __init__(self, name : str, description : str, action : Callable, condition : Callable[[], bool] = lambda : True, passTurn=True, failFeedback="the action cant be executed, something is missing."):
        self.name = name
        self.description = description
        self.action = action
        self.condition = condition
        self.passTurn = passTurn
        self.room = None
        self.failFeedback = failFeedback


    async def __call__(self, channel : discord.TextChannel, executioner : Player.Player):

        if self.condition():
            await Functions.CallAction(self.action, channel, executioner)
            return not self.passTurn
        else:
            await channel.send(self.failFeedback)
            return False


