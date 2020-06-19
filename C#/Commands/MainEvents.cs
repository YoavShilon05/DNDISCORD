using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using DSharpPlus.EventArgs;


namespace CSDNDISCORD
{
    static class MainEvents
    {
        public static Task OnClientReady(ReadyEventArgs e)
        {
            Console.WriteLine("bot is ready");
            return null;
        }
    }
}
