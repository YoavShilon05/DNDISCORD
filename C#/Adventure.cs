using System;
using System.Collections.Generic;
using System.Text;
using DSharpPlus;
using DSharpPlus.Entities;
using System.Threading;

namespace CSDNDISCORD
{
    class Adventure
    {

        public string name;
        public List<Room> rooms;
        public int minPartySize;
        public int maxPartySize;

        public List<Command> commands;
        public Dictionary<string, Object> vars;
        public Party party { get; private set; }
        
        public Player currentPlayer;
        private int turnIndex = 0;

        public bool useVoice { get; private set; }
        public bool connectedToVoice { get; private set; }
        public bool playingBackgroundMusic { get; private set; }
        public string backgroundTrack { get; private set; }

        public DiscordChannel channel;


        public Adventure(string name, int minPartySize, int maxPartySize, bool voice = true)
        {

            this.name = name;
            this.minPartySize = minPartySize;
            this.maxPartySize = maxPartySize;

            this.useVoice = voice;
            currentPlayer = party.players[0];

            bool tst(Player player)
            {
                this.channel.SendMessageAsync("test");
                return false;
            }

            commands.Add(new Command(tst, "test..."));

        }

        public void PassTurn()
        {
            turnIndex++;
            if (turnIndex == party.players.Count)
            {
                turnIndex = 0;
            }
            currentPlayer = party.players[turnIndex];
        }
    }

    class Command
    {
        string name;
        string description;
        Func<Player, bool> command;
        List<string> aliases;

        public Command(Func<Player, bool> command, string description = "", List<string> aliases = null)
        {
            
            if (aliases == null)
            {
                aliases = new List<string>();
            }

            name = command.Method.Name;
            this.description = description;
            this.command = command;
            this.aliases = aliases;

        }
        

        public bool Invoke(Player player)
        {
            return this.command(player);
        }

        
    }

    class Room
    {
        public string name;
        public Sequence fullDescription;
        public Sequence shortDescription;
        public List<Operation> operations = new List<Operation>();
        private Dictionary<Item, Action<Player>> itemoperations = new Dictionary<Item, Action<Player>>();
        public List<Item> items { get; private set; }
        public Adventure adventure { get; private set; }
        public List<Player> players { get; private set; } = new List<Player>();
        public Action<Player> onEnter;
        public Action<Player> onLeave;
        private bool entered = false;
        public Room(string name, Sequence fullDescription, Sequence shortDescription = null, 
            List<Item> items = null, Action<Player> onEnter = null, Action<Player> onLeave = null)
        {
            void EmptyMethod(Player player)
            {
                Console.WriteLine(player.name + " called an empty method.");
            }

            if (onEnter == null) { onEnter = EmptyMethod; }
            if (onLeave == null) { onLeave = EmptyMethod; }
            if (shortDescription == null) { shortDescription = fullDescription; }
            if (items == null) { items = new List<Item>(); }

            this.name = name;
            this.fullDescription = fullDescription;
            this.shortDescription = shortDescription;
            this.onEnter = onEnter;
            this.onLeave = onLeave;
            
            foreach (Item i in items) { AddItem(i); }
        }

        public void AddItem(Item item)
        {
            this.items.Add(item);

            async void TakeItem(Player player)
            {
                player.character.inventory.AddItem(item);
                string a;
                if (new List<char> { 'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U' }.Contains(item.rarity.ToString()[0]))
                { a = "an"; } else { a = "a"; }

                if (player.character.inventory.empty) { await player.adventure.channel.SendMessageAsync("Inventory is full"); }
                else
                {
                    await player.adventure.channel.SendMessageAsync(player.character.name + " has taken " + a + " " +
                item.rarity.ToString() + " " + item.name + ".");
                }
            }

            itemoperations.Add(item, TakeItem);
        }
        public void RemoveItem(Item item) 
        {
            items.Remove(item);
            itemoperations.Remove(item);
        }

        public string GetOperationRepr(Player player)
        {
            int spaces = 8;
            string result = "actions: \n";
            for (int o = 0; o < this.operations.Count; o++)
            {
                Operation operation = this.operations[o];

                if (operation.condition.Invoke(player))
                {
                    string addToResult = (o + 1).ToString() + ". - ";

                    if (operation.emoji != null)
                    { addToResult += operation.emoji; }
                    else { addToResult += "/// "; }

                    addToResult += operation.name;
                    
                    if (operation.description != null)
                    { addToResult += new String('d', spaces).Replace("d", " - ") + operation.description; }
                    
                    addToResult += operation.name + new String('d', spaces).Replace("d", " - ") + operation.description + "\n";
                    result += addToResult + "\n";
                }
            }

            result += "\nitems: \n";

            foreach(Item item in items) { result += item.name; }

            return result;
        }

        public async void Enter(Player player)
        {

            players.Add(player);

            if (player.character.room != null) { player.character.room.Leave(player); }
            player.character.room.Leave(player);
            player.character.room = this;

            this.onEnter(player);
            if (!entered)
            { fullDescription.Play(this.adventure.channel); entered = true; } 
            else { shortDescription.Play(this.adventure.channel); }

            await this.adventure.channel.SendMessageAsync(this.GetOperationRepr(player));

            await Program.bot.Interactivity.WaitForMessageAsync(m => m.Content == "");

        }

        public void Leave(Player player)
        {

        }


    }

    struct Operation
    {
        public Func<Player, bool> function { get; private set; }
        public string name;
        public string description;
        public Func<Player, bool> condition;
        public string emoji;

        public Operation(Func<Player, bool> function, string description = null, string emoji = null, Func<Player, bool> condition = null)
        {
            this.function = function;
            name = function.Method.Name;
            this.description = description;
            this.emoji = emoji;
            if (condition == null) { condition = p => true; }
            this.condition = condition;
        }

    }

    class Sequence
    {
        public struct Item
        {
            public string text;
            public string backgroundTrack;
            public bool waitForReaction;
            public int delay;
            public bool delete;

            public Item(string text, string backgroundTrack, bool waitForReaction=true, 
                int delay = 0, bool delete=false)
            {
                this.text = text;
                this.backgroundTrack = backgroundTrack;
                this.waitForReaction = waitForReaction;
                this.delay = delay;
                this.delete = delete;
            }

        }

        public Room room;
        public List<Item> items;
        
        public Sequence(List<Item> items)
        {
            this.items = items;
        }

        public async void Play(DiscordChannel channel)
        {
            foreach (Item i in items)
            {

                DiscordMessage msg = await channel.SendMessageAsync(i.text);
                
                if (i.waitForReaction)
                {
                    await msg.CreateReactionAsync(DiscordEmoji.FromName(Program.bot.Client, ":track_next:"));
                    await Program.bot.Interactivity.WaitForReactionAsync(
                        r => r.User.IsBot == false && r.Emoji.GetDiscordName() == ":track_next:");
                } else
                {
                    Thread.Sleep(i.delay);
                }

                if (i.delete) { await msg.DeleteAsync(); }


            }
        }
    }

}
