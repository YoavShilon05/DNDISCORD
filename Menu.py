import discord
from GlobalVars import bot
from typing import Callable, List
from Player import Player


backEmoji = "🔙"


class Menu():

    def __init__(self, content:str, emoji, childMenus, embed=None, file=None, deleteAfter:float=None):

        self.content = content
        self.emoji = emoji
        self.embed = embed
        self.file = file
        self.deleteAfter = deleteAfter
        self.childMenus : List[Menu] = childMenus
        self.parentMenu : Menu = None

        for m in self.childMenus:
            m.parentMenu = self

    async def Send(self, channel : discord.TextChannel, sender : Player):

        message = await channel.send(content=self.content, embed=self.embed, file=self.file,
                     delete_after=self.deleteAfter)

        for m in self.childMenus:
            await message.add_reaction(m.emoji)
        await message.add_reaction(backEmoji)


        menuEmojis = [m.emoji for m in self.childMenus]
        reaction, user = await bot.wait_for('reaction_add', check=lambda r, u : ((r.emoji in menuEmojis) or (r.emoji == backEmoji)) and u == sender)

        if reaction.emoji == backEmoji:
            if self.parentMenu != None:
                await self.parentMenu.Send(channel, sender)
                return

        targetMenu = [menu for menu in self.childMenus if menu.emoji == reaction.emoji][0]

        await targetMenu.Send(channel, user)

class Entrance(Menu):

    def __init__(self, content:str, emoji, function : Callable[[List[Player]], None], embed=None, file=None, deleteAfter:float=None):
        super().__init__(content, emoji, [], embed, file, deleteAfter)
        self.function = function