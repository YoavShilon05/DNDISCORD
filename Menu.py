import discord
import GlobalVars
from typing import Callable, List
from Player import Player
from Functions import CallAction

backEmoji = "🔙"


class Menu():

    def __init__(self, content:str, emoji, childMenus, description=None, embed=None, file=None, deleteAfter:float=None):

        self.content = content
        self.description = description if description != None and description else ""
        self.emoji = emoji
        self.embed = embed
        self.file = file
        self.deleteAfter = deleteAfter
        self.childMenus : List[Menu] = childMenus
        self.parentMenu : Menu or None = None

        for m in self.childMenus:
            m.parentMenu = self

    async def Send(self, channel : discord.TextChannel, sender : Player):

        spaces = 8

        message = await channel.send(content=self.content + (spaces * " - " + self.description if self.description != "" else "") +
                                             "\n" + "\n".join([f"{c.emoji + spaces * ' - '}`{c.content}`{' - ' if c.description != '' + c.description else ''}"
                                                               for c in self.childMenus]),
                                     embed=self.embed, file=self.file,
                     delete_after=self.deleteAfter)

        for m in self.childMenus:
            await message.add_reaction(m.emoji)
        if self.parentMenu != None:
            await message.add_reaction(backEmoji)


        menuEmojis = [m.emoji for m in self.childMenus]
        reaction, user = await GlobalVars.bot.wait_for('reaction_add', check=lambda r, u : ((r.emoji in menuEmojis) or (r.emoji == backEmoji)) and u == sender.author)

        await message.delete(delay=0.35)

        if reaction.emoji == backEmoji:
            await self.parentMenu.Send(channel, sender)
        else:
            await [m for m in self.childMenus if m.emoji == reaction.emoji][0].Send(channel, sender)


class Starter(Menu):

    def __init__(self, content:str, emoji, function : Callable, embed=None, file=None, deleteAfter:float=None):
        super().__init__(content, emoji, [], embed, file, deleteAfter)
        self.function = function

    async def Send(self, channel : discord.TextChannel, sender : Player):

        message = await channel.send(content=self.content, embed=self.embed, file=self.file,
                                     delete_after=self.deleteAfter)
        if self.parentMenu != None:
            await message.add_reaction(backEmoji)
        await message.add_reaction(self.emoji)


        reaction, user = await GlobalVars.bot.wait_for('reaction_add', check=lambda r, u: (r.emoji == self.emoji or (r.emoji == backEmoji)) and u == sender.author)

        await message.delete(delay=0.35)

        if reaction.emoji == backEmoji:
            await self.parentMenu.Send(channel, sender)

        else:
            await CallAction(self.function, message, GlobalVars.players[user.id])