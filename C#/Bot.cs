using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using DSharpPlus;
using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;
using DSharpPlus.Interactivity;

namespace CSDNDISCORD
{
    class Bot
    {
        public DiscordClient Client { get; private set; }
        public CommandsNextExtension Commands {get; private set;}

        public InteractivityExtension Interactivity { get; private set; }

        public async Task Run()
        {
            var config = new DiscordConfiguration
            {
                Token = "NzE0ODQ1NzIxMTk4NTkyMDYx.Xs6hWQ.KNM0bNjcrGcNTL0pAYiuh06sahk",
            };

            Client = new DiscordClient(config);

            var CommandsConfig = new CommandsNextConfiguration
            {
                StringPrefixes = new string[] {"c."}
            };

            Commands = Client.UseCommandsNext(CommandsConfig);

            Interactivity = Client.UseInteractivity(new InteractivityConfiguration());
            

            await Client.ConnectAsync();

            //register commands
            Commands.RegisterCommands<MainCommands>();

            //register events
            Client.Ready += MainEvents.OnClientReady;

            await Task.Delay(-1);

        }
    }
}
