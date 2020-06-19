from discord.ext.commands import Bot
import discord
from typing import *


class a:

    b = 323

    @staticmethod
    def A():
        print(a.b)



bot : Bot = None
botVoiceClients : Dict[discord.Guild, discord.VoiceClient] = {}
players = {}
