using System;
using System.Collections.Generic;
using System.Text;

namespace CSDNDISCORD
{
    class Character
    {
        public string name;
        public Sexes sex;
        public Races race;
        public Professions profession;

        public float maxHealth;
        public float health;
        public float damage;

        public string backstory;
        public Inventory inventory;
        public Weapon mainWeapon;
        public Room room;



    }

    enum Sexes
    {
        male,
        female,
        unknown
    }

    enum Races
    {
        
    }

    enum Professions
    {

    }

    class Inventory
    {
        public bool empty;
        public void AddItem(Item item) { }
    }

    class Item
    {
        public string name;
        public string description;
        public Rarities rarity;
    }

    enum Rarities
    {
        common,
        uncommon,
        rare,
        epic,
        legendary,
    }

    class Usable : Item
    {

    }

    class Weapon : Item
    {

    }
}
