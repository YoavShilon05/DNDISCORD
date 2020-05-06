from Inventory import Inventory
import enum

class Sexes(enum.Enum):
    male = 0
    female = 1
    unknown = 2



class Entity:
    def __init__(self, name, sex : Sexes, race, backstory=""):
        self.name = name
        self.sex = sex

        self.race = race

        #TODO: make health & dmage be affected by races & profession.
        self.maxHealth = 25
        self._health = 5
        self.damage = 15

        self.backstory = backstory
        self.inventory = Inventory(self, 2, 7)
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

    async def Attack(self):
        pass

class Character(Entity):

    def __init__(self, name, sex, race, profession, backstory=""):
        super().__init__(name, sex, race, backstory)

        self.race = race
        self.profession = profession