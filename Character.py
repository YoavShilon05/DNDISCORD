import Inventory

class Entity:
    def __init__(self, name, maxHealth, startHealth, damage, backstory=""):
        self.name = name
        self.damage = damage
        self.maxHealth = maxHealth
        self._health = startHealth
        self.backstory = backstory
        self.inventory = Inventory.Inventory(self, 6)
        self.mainWeapon = None

    def _HealthGetter(self):
        return self._health

    def _HealthSetter(self, val):
        if self._health + val > self.maxHealth:
            raise ValueError("Health over max Health")
        else:
            self._health += val

    health = property(_HealthGetter, _HealthSetter)

