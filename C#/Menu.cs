using System;
using System.Collections.Generic;
using System.Text;
using DSharpPlus.Entities;


namespace CSDNDISCORD
{

    class Menu
    {
        public string name { get; private set; }
        public string description { get; private set; }
        public string emoji { get; private set; }
        public List<Menu> childMenus { get; private set; }
        public Func<Player, bool> operation { get; private set; }
        public Func<Player, bool> counterOperation { get; private set; }
        public bool showDescription { get; private set; }
        public Menu parentMenu { get; private set; } = null;
        public bool empty { get; private set; }

        public static int spaces = 8;
        public static string backemoji = ":back:";

        public Menu(string title, string description, string emoji, List<Menu> childMenus, Func<Player, bool> action = null, Func<Player, bool> counterAction = null, bool empty=false,
            bool showDescription = true)
        {
            this.name = title;
            this.description = description;
            this.emoji = emoji;
            this.childMenus = childMenus;
            this.operation = action;
            this.counterOperation = counterAction;
            this.showDescription = showDescription;
            this.empty = empty;

            foreach(Menu m in this.childMenus)
            {
                m.parentMenu = this;
            }

        }


        public async void Send(DiscordChannel channel, Player sender)
        {
            bool sendMessage = true;
            if (this.operation != null) sendMessage = this.operation.Invoke(sender);

            if (!sendMessage || empty) return;


            string title = this.name;
            if (this.showDescription == true)
            {

                title += " - ";
                title += this.description;
            }

            string description = "";
            foreach (Menu m in this.childMenus)
            {
                description += m.emoji;
                description += new String('d', spaces).Replace("d", " - ");
                description += "`" + m.name + "`";
                description += "\n";
            }

            DiscordMessage msg = await channel.SendMessageAsync(title + "\n" + description);

            List<string> reactions = new List<string>();

            foreach (Menu m in this.childMenus)
            {
                await msg.CreateReactionAsync(DiscordEmoji.FromName(Program.bot.Client, m.emoji));
                reactions.Add(m.emoji);
            }
            if (this.parentMenu != null)
            {
                await msg.CreateReactionAsync(DiscordEmoji.FromName(Program.bot.Client, backemoji));
                reactions.Add(backemoji);
            }

            

            var reactionResult = await Program.bot.Interactivity.WaitForReactionAsync(r => !r.User.IsBot && (reactions.Contains(r.Emoji.GetDiscordName())));

            if (reactionResult.Result != null)
            {
                if (reactionResult.Result.Emoji.GetDiscordName() == backemoji)
                {
                    this.counterOperation.Invoke(sender);
                    this.parentMenu.Send(channel, sender);
                }
                else
                {
                    foreach (Menu m in this.childMenus)
                    {
                        if (m.emoji == reactionResult.Result.Emoji.GetDiscordName())
                        {
                            m.Send(channel, sender);
                            break;
                        }
                    }
                }
            }
            await msg.DeleteAsync();
        }

        public void AddChild(Menu child)
        {
            this.childMenus.Add(child);
        }
    }

}
