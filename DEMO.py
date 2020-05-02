import Inventory
import Character
import Races

MainCharac = Character.Character("name", 20, 15, Races.races.elf, None)

MCInventory = Inventory.Inventory(MainCharac, 6)

def foo(player):
    player.health += 8

Steak = Potion.Poiton("Steak", "steak...", foo)
MCInventory.AddItem(Steak)


while True:


    i = input("> ")

    if i == "inv":
        print(str(MCInventory))

    elif i == "use":
        MCInventory.UseItem(MCInventory.items[0])

    elif i == "health" or i == "hp":
        print(MainCharac.health)

    elif i == "steak":
        MCInventory.AddItem(Steak)