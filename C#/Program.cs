using System;
using System.Collections.Generic;
using DSharpPlus;
using DSharpPlus.Entities;

namespace CSDNDISCORD
{
    static class Program
    {
        public static Dictionary<DiscordUser, Player> Players;

        public static Bot bot = new Bot();
        static void NOTMain(string[] args)
        {
            bot.Run().GetAwaiter().GetResult();



        }
    }
}
