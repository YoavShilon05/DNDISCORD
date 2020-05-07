'''
import Item
import random
from typing import List


#Buffers - will be a dict: key is Name, value is a tuple - (damage, description)
#Race Buffers - will be a dict: key is Name, value is a tuple - (damage, Race, description)

class Weapon(Item.Item):

    def __init__(self, name, description, minDamage, maxDamage, buffers : List[Buffers.Buffer], raceBuffers : List[Buffers.RaceBuffer]):

        super().__init__(name, description)

        self.minDamage = minDamage
        self.maxDamage = maxDamage

        self.buffers = List[Buffers.Buffer]
        self.buffers = buffers
        self.raceBuffers = List[Buffers.RaceBuffer]
        self.raceBuffers = raceBuffers

    def DealDamage(self, enemy, dice, diceValue, randommRange=0):

        Buffers = sum(b.damage for b in self.buffers)

        #syntax might be wrong, dice not written yet.

        for rbuffer in self.raceBuffers:
            if enemy.race in rbuffer.races:
                Buffers += rbuffer.damage

        diceRatio = diceValue / dice.sides

        return Buffers + self.minDamage + diceRatio * (self.maxDamage - self.minDamage) + random.randint(-round(randommRange/2), round(randommRange/2))

    def AddBuffer(self, buffer : Buffers.Buffer):
        if type(buffer) is Buffers.Buffer:
            self.buffers.append(buffer)
        else:
            self.raceBuffers.append(buffer)

    def RemoveBuffer(self, buffer : Buffers.Buffer):
        if type(buffer) is Buffers.Buffer:
            self.buffers.remove(buffer)
        else:
            self.raceBuffers.remove(buffer)

'''