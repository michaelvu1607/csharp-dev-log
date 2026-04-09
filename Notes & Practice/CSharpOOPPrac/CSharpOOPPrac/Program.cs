using System;
using System.Collections.Generic;

namespace CSharpOOPPrac
{
    class Program
    {
        static void Main(string[] args)
        {
            List<string> food = new List<string>();
            food.Add("pizza");
            food.Add("hamburger");
            food.Add("hotdog");

            food.Insert(0, "sushi");
            food.Remove("pizza");
            Console.WriteLine(food.Count);
            Console.WriteLine(food.IndexOf("hamburger"));
            
            foreach (string i in food)
            {
                Console.WriteLine(i);
            }
            
            Console.ReadKey();
        }
    }
}