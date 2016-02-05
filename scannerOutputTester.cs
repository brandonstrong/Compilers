using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using Antlr.Runtime.Debug;
using System.IO;
namespace ConsoleTester
{
    class Program
    {        
        static void Main(string[] args)
        {
            try
            {
                StreamReader ourStream = new StreamReader(@"C:\Users\Brandons\Desktop\our_outputs\loop.txt");
                StreamReader theirStream = new StreamReader(@"C:\Users\Brandons\Desktop\outputs\loop.txt");

                string ourLine = "";
                string theirLine = "";

                int linecount = 1;

                while ((ourLine = ourStream.ReadLine()) != "Value: END" && (theirLine = theirStream.ReadLine()) != "Value: END")
                {
                    if (ourLine.Equals(theirLine))
                    {
                        Console.WriteLine(ourLine);
                        linecount++;
                    }
                    else
                    {
                        throw new Exception("Outputs differ at line " + linecount + ".\nOur line: " + ourLine + ", Their line: " + theirLine);
                    }                    
                }
                Console.WriteLine(ourLine + "\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }

            Console.WriteLine("Press escape to exit");
            while (Console.ReadKey().Key != ConsoleKey.Enter) ;
        }
    }
    
}
