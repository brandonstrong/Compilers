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
                //string file = "fibonacci";
                //string file = "loop";
                //string file = "nested";
                string file = "sqrt";
                StreamReader ourStream = new StreamReader(@"C:\Users\" + Environment.UserName + @"\Desktop\step1\our_outputs\" + file + ".txt");
                StreamReader theirStream = new StreamReader(@"C:\Users\" + Environment.UserName + @"\Desktop\step1\outputs\" + file + ".txt");

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
            while (Console.ReadKey().Key != ConsoleKey.Escape) ;
        }
    }
    
}
