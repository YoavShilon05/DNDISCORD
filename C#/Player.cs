using System;
using System.Collections.Generic;
using System.Text;
using DSharpPlus.Entities;
using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;

namespace CSDNDISCORD
{
    class Player
    {
        public DiscordMember member;
        public string name;
        public string username;
        public List<Character> characters = new List<Character>();

        public Adventure adventure = null;
        public HashSet<Adventure> adventuresPlayed = new HashSet<Adventure>();

        public Party party = null;
        public Character character;

        public Player(DiscordMember member, string username = "")
        {
            this.member = member;
            this.name = member.DisplayName;
            this.username = username;
        }

        public async void LeaveParty(CommandContext ctx)
        {
            if (party == null) { await ctx.Channel.SendMessageAsync("You are not in a party."); return; }
            party.players.Remove(this);
            if (party.leader == this) { party.leader = party.players[0]; 
                await ctx.Channel.SendMessageAsync("Left the party."); }
            
        }
    }

    class Party
    {
        public List<Player> players { get; private set; } = new List<Player>();
        public Player leader;

        public Party(List<Player> players)
        {
            this.players = players;
            leader = players[0];
        }

        public void AddPlayer (Player player)
        {
            players.Add(player);
            player.party = this;
        }

        public async void Kick (CommandContext ctx, Player player)
        {
            if (!players.Contains(player))
            {
                await ctx.Channel.SendMessageAsync("Player not in party");
                return;
            }
            if (player == leader)
            {
                await ctx.Channel.SendMessageAsync("You can't kick the party leader.");
            } else
            {
                players.Remove(player);
                await ctx.Channel.SendMessageAsync("Kicked " + player.member.Mention + " from the party");
                await player.member.SendMessageAsync("You were kicked from " + leader.member.Mention + "'s party");
            }
        }
    }
}
