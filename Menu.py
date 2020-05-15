import discord
import GlobalVars
from typing import Callable, List
from Player import Player
from Functions import CallAction

backEmoji = "🔙"


class Menu():

    def __init__(self, content:str, emoji, childMenus, description=None, **properties):

        self.content = content
        self.description = description if description != None and description else ""
        self.emoji = emoji
        self.embed = properties.get('embed', None)
        self.file = properties.get('file', None)
        self.deleteAfter = properties.get('deleteAfter', None)
        self.childMenus : List[Menu] = childMenus
        self.parentMenu : Menu or None = None
        self.showChildMenuDescriptions = properties.get('showChildMenuDescriptions', False)
        self.showDescription = properties.get('showDescription', True if type(self) == Starter else False)

        for m in self.childMenus:
            m.parentMenu = self

    async def Send(self, channel : discord.TextChannel, sender : Player):

        spaces = 8

        title = f"`{self.content}{( ' - ' + self.description if self.description != '' and self.showDescription else '')}`"
        description = "\n".join([f"{c.emoji + spaces * ' - '}`{c.content}`"
                                 f"{' - ' + c.description if c.description != '' and c.showChildMenuDescriptions else ''}"
                                         for c in self.childMenus])
        sendMessage = title + "\n" + description

        message = await channel.send(content=sendMessage,
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

    def __init__(self, content:str, emoji, function : Callable, description=None, **properties):
        super().__init__(content, emoji, [], description, **properties)
        self.function = function

    async def Send(self, channel : discord.TextChannel, sender : Player):

        title = f"`{self.content}\n{(self.description if self.description != '' and self.showDescription else '')}`"

        message : discord = await channel.send(content=title, embed=self.embed, file=self.file,
                                     delete_after=self.deleteAfter)
        if self.parentMenu != None:
            await message.add_reaction(backEmoji)
        await message.add_reaction(self.emoji)


        reaction, user = await GlobalVars.bot.wait_for('reaction_add', check=lambda r, u: (r.emoji == self.emoji or (r.emoji == backEmoji)) and u == sender.author)


        if reaction.emoji == backEmoji:
            await self.parentMenu.Send(channel, sender)
            await message.delete(delay=0.35)

        else:
            await CallAction(self.function, message.channel, GlobalVars.players[user.id])