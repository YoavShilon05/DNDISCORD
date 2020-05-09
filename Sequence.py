from asyncio import sleep
import discord
import GlobalVars

sfx = {
    #add sfx here
}

passEmoji = '▶️'

class Sequence:
    def __init__(self, items : list or tuple, *, deleteMessages=True):
        self.waitForReaction = True
        #TODO: make sure al items of sequenc eare of the same type.
        for item in items:
            if type(item) is list or type(item) is tuple:
                if type(item[-1]) is float or type(item[-1]) == int:
                    self.waitForReaction = False
                    break
        self.sequence = items
        self.deleteMsgs = deleteMessages
        self.room = None

    async def Play(self, channel : discord.TextChannel):
        for item in self.sequence:
            msg = None

            #TODO: if there's sound play it

            if (type(item) == list or type(item) == tuple):
                if type(item[1]) is str:
                    adventure = self.room.adventure
                    if adventure.useVoice:
                        voiceClient : discord.VoiceClient = GlobalVars.botVoiceClients[channel.guild]
                        if voiceClient.is_playing():
                            voiceClient.stop()
                        voiceClient.play(discord.FFmpegPCMAudio(item[1]))


            if self.waitForReaction:
                message = item
                if type(message) == list or type(message) == tuple:
                    message = item[0]
                msg = await channel.send(message)
                await msg.add_reaction(passEmoji)
                reaction, user = await GlobalVars.bot.wait_for('reaction_add', check=lambda r, u : r.message.id == msg.id and r.emoji == passEmoji and not u.bot)


            else:
                msg = await channel.send(item[0])
                await sleep(item[-1])

            if self.deleteMsgs:
                await msg.delete()

        adventure = self.room.adventure
        if adventure.useVoice:
            voiceClient: discord.VoiceClient = GlobalVars.botVoiceClients[channel.guild]
            if voiceClient.is_playing():
                voiceClient.stop()