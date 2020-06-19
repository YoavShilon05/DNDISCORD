import discord
import GlobalVars
from typing import Callable, List, Awaitable
from Player import Player

backEmoji = "🔙"


class Menu:

    def __init__(self, title:str, emoji, childMenus, description=None,
                 action : Callable[[discord.TextChannel, Player], Awaitable[bool]]=None,
                 counterAction : Callable[[discord.TextChannel, Player], Awaitable[bool]]=None, **properties):

        self.title : str = title
        self.description : str = description if description != None and description else ""
        self.emoji : str = emoji
        self.action : Callable[[discord.TextChannel, Player], Awaitable[bool]] = action
        self.counterAction : Callable[[discord.TextChannel, Player], Awaitable[bool]] = counterAction

        self.embed : discord.Embed = properties.get('embed', None)
        self.deleteAfter : float = properties.get('deleteAfter', None)
        self.childMenus : List[Menu] = childMenus
        self.parentMenu : Menu = None
        self.showDescription = properties.get('showDescription', False)

        for m in self.childMenus:
            m.parentMenu = self

    async def Send(self, channel : discord.TextChannel, sender : Player):

        if self.action != None:
            result = await self.action(channel, sender)
            if not result:
                return

        spaces = 8

        title = f"`{self.title}{(' - ' + self.description if self.description != '' and self.showDescription else '')}`"
        description = "\n".join([f"{c.emoji + spaces * ' - '}`{c.title}`"
                                         for c in self.childMenus])
        sendMessage = title + "\n" + description

        message = await channel.send(content=sendMessage,
                                     embed=self.embed,
                     delete_after=self.deleteAfter)

        for m in self.childMenus:
            await message.add_reaction(m.emoji)
        if self.parentMenu != None:
            await message.add_reaction(backEmoji)


        menuEmojis = [m.emoji for m in self.childMenus]
        reaction, user = await GlobalVars.bot.wait_for('reaction_add', check=lambda r, u : ((r.emoji in menuEmojis) or (r.emoji == backEmoji)) and u == sender.author)

        await message.delete(delay=0.35)

        if reaction.emoji == backEmoji:
            if self.counterAction != None:
                sendParent = await self.counterAction(sender)
                if sendParent:
                    await self.parentMenu.Send(channel, sender)
                return

            await self.parentMenu.Send(channel, sender)
        else:
            await [m for m in self.childMenus if m.emoji == reaction.emoji][0].Send(channel, sender)

