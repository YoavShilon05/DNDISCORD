from discord.ext.commands import Bot
import discord
from typing import *


bot : Bot = None
botVoiceClients : Dict[discord.Guild, discord.VoiceClient] = {}
players = {}