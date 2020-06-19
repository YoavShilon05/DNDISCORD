using System;
using System.Collections.Generic;
using System.Text;
using System.Diagnostics;

namespace TEST
{
    class TEST
    {

        static List<string> a = new List<string>(new string[] {"12", "2"});
        static int[] b = new int[400];

        public static void Main()
        { 
            
            var f = typeof(A).GetFields();
            var p = typeof(A).GetProperties();
            var m = typeof(A).GetMembers();
            var meth = typeof(A).GetMethods();

            Console.WriteLine(f.Length);
            Console.WriteLine(f[0]);
            Console.WriteLine(f);
            Console.WriteLine(p.Length);
            Console.WriteLine(p[0]);
            Console.WriteLine(p);

            Console.WriteLine(m.Length);
            Console.WriteLine(m);            
            foreach(var member in m)
            {
                Console.WriteLine(member);
            }


            Console.WriteLine(meth.Length);
            Console.WriteLine(meth);
            foreach (var method in meth)
            {
                Console.WriteLine(method);
            }

        }


    }

    class A
    {
        public string member = "tst";

        public string property { get; private set; } = "tst";

        public string method()
        {
            return "tst";
        }
    }
}