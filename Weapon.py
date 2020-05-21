
import Item
import random
from typing import List


#Buffers - will be a dict: key is Name, value is a tuple - (damage, description)
#Race Buffers - will be a dict: key is Name, value is a tuple - (damage, Race, description)

class Weapon(Item.Item):

    def __init__(self, name, description, damage):

        super().__init__(name, description)

        self.damage = damage