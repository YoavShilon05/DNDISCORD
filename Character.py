import Inventory

class Entity:
    def __init__(self, name, damage, backstory=""):
        self.name = name
        self.damage = damage

        #TODO: make health & dmage be affected by races & profession.

        self.maxHealth = 25
        self._health = 5
        self.backstory = backstory
        self.inventory = Inventory.Inventory(self, 2, 7)
        self.mainWeapon = None

    def _HealthGetter(self):
        return self._health

    def _HealthSetter(self, val):
        if self._health + val > self.maxHealth:
            self._health = self.maxHealth
            print("Health was set to over max, set it back to max.")
        else:
            self._health += val

    health = property(_HealthGetter, _HealthSetter)

class Character(Entity):

    def __init__(self, name, race, profession, backstory=""):
        super().__init__(name, backstory)

        self.race = race
        self.profession = profession