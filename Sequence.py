from asyncio import sleep

class Sequence:

    def __init__(self, Sequence):
        self.sequence = Sequence

    async def play(self, channel):
        for item in self.sequence:
            await channel.send(item[0])
            await sleep(item[1])