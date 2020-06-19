import Item
from typing import List
import Character

class Fight:
    def __init__(self, characters, monsters, loot : List[Item.Item]):

        self.characters = characters
        self.monsters = monsters
        self.loot = loot


    def Attack(self, enemies: List[Character.Monster], damage, **properties):
        radialSubtraction = 0
        if 'radialSubtraction' in properties:
            radialSubtraction = properties['radialSubtraction']
        currentDamage = damage

        for p in enemies:
            p.health -= currentDamage
            currentDamage -= radialSubtraction

            if p.health == 0:
                p.Kill()
                self.monsters.remove(p)
                del p

