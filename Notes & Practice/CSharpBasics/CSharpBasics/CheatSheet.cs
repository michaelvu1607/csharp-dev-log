using System;

// #1 (00:00:00) C# tutorial for beginners
// C# requires a namespace and a class. The execution always starts in 'static void Main'.
namespace CSharpFullCheatSheet
{
    class Program
    {
        static void Main(string[] args)
        {
            // ==========================================
            // #2 (00:06:30) output
            // Python: print("Hello")
            // C# requires semicolons (;) at the end of every statement!
            Console.WriteLine("Hello World!"); // Prints and adds a new line
            Console.Write("I am on the ");     // Prints without a new line
            Console.Write("same line!\n");

            // ==========================================
            // #3 (00:10:48) variables
            // Python is dynamically typed (x = 5). C# is statically typed.
            int x = 5;                   // Whole numbers
            double y = 3.14;             // Decimals (like Python float)
            bool isAlive = true;         // Note the lowercase 't' and 'f'
            char symbol = '@';           // Single character MUST use single quotes ''
            string name = "Bro";         // Text MUST use double quotes ""

            // ==========================================
            // #4 (00:19:32) constants
            // Python uses ALL_CAPS as a naming convention. C# enforces it so it can't be changed.
            const double PI = 3.14159;

            // ==========================================
            // #5 (00:20:35) type casting
            // Python: str(3), int("5")
            double a = 3.14;
            int b = Convert.ToInt32(a);         // Converts double to int (3)
            string c = Convert.ToString(b);     // Converts int to string ("3")

            // ==========================================
            // #6 (00:27:49) user input
            // Python: input("Prompt: ")
            // Note: I am commenting this out so it doesn't pause your IDE when you test run!
            /*
            Console.WriteLine("What is your age?");
            int age = Convert.ToInt32(Console.ReadLine()); // ReadLine ALWAYS returns a string
            */

            // ==========================================
            // #7 (00:31:24) arithmetic operators
            // Python: x += 1
            int friends = 5;
            friends = friends + 1;
            friends += 1;
            friends++; // C# shortcut to add exactly 1
            friends--; // C# shortcut to subtract exactly 1

            // ==========================================
            // #8 (00:35:54) Math class
            double mathNum = 3.99;
            double rounded = Math.Round(mathNum); // 4
            double ceiling = Math.Ceiling(mathNum); // Always rounds up
            double floor = Math.Floor(mathNum);   // Always rounds down
            double max = Math.Max(5, 10);         // Returns 10

            // ==========================================
            // #9 (00:40:55) random numbers
            // Python: import random
            Random random = new Random();
            int randomNum = random.Next(1, 7); // Generates 1 through 6 (7 is exclusive)

            // ==========================================
            // #10 (00:44:27) hypotenuse calculator program
            double sideA = 3;
            double sideB = 4;
            double sideC = Math.Sqrt((sideA * sideA) + (sideB * sideB)); // 5

            // ==========================================
            // #11 (00:46:35) string methods
            // Python: len(fullName)
            string fullName = "Bro Code";
            int nameLength = fullName.Length; 
            string upper = fullName.ToUpper();
            string sub = fullName.Substring(0, 3); // Extracts "Bro"

            // ==========================================
            // #12 (00:53:26) if statements
            // Python uses colons and indentation. C# uses parentheses () and braces {}.
            int temp = 25;
            if (temp > 30) {
                Console.WriteLine("Hot");
            } 
            else if (temp > 15) { // Python: elif
                Console.WriteLine("Warm");
            } 
            else {
                Console.WriteLine("Cold");
            }

            // ==========================================
            // #13 (00:59:43) switches
            // Great for checking one variable against many specific values.
            string day = "Friday";
            switch (day) {
                case "Monday": Console.WriteLine("It's Monday"); break;
                case "Friday": Console.WriteLine("It's Friday!"); break;
                default: Console.WriteLine("Another day"); break; // Python: else
            }

            // ==========================================
            // #14 (01:02:50) logical operators && ||
            // Python: and, or, not
            // && (AND), || (OR), ! (NOT)
            if (temp >= 15 && temp <= 30) {
                Console.WriteLine("Perfect weather!");
            }

            // ==========================================
            // #15 (01:06:36) while loops
            int count = 0;
            while (count < 3) {
                count++;
            }

            // ==========================================
            // #16 (01:09:45) for loops
            // Python: for i in range(5):
            // Setup: (declare counter; condition; increment)
            for (int i = 0; i < 5; i++) {
                Console.WriteLine($"Loop {i}");
            }

            // ==========================================
            // #17 (01:13:24) nested loops
            for (int i = 0; i < 2; i++) {
                for (int j = 0; j < 2; j++) {
                    // Prints a 2x2 grid pattern
                    Console.Write("*");
                }
                Console.WriteLine();
            }

            // ==========================================
            // #18, #19, #20: THE MINI PROGRAMS
            // Wrapped in if(false) so they don't block your cheat sheet from running.
            // Change to true if you want to test them.
            if (false) 
            {
                // #18 (01:18:28) number guessing game
                int answer = random.Next(1, 100);
                int guess = 0;
                while (guess != answer) {
                    guess = Convert.ToInt32(Console.ReadLine());
                    if (guess > answer) Console.WriteLine("Too high!");
                }

                // #19 (01:27:08) rock-paper-scissors game
                string player = "ROCK"; // Normally from ReadLine
                string cpu = "PAPER";   // Normally generated by Random
                switch(player) {
                    case "ROCK":
                        if (cpu == "ROCK") Console.WriteLine("Draw");
                        else if (cpu == "PAPER") Console.WriteLine("You Lose");
                        break;
                }

                // #20 (01:38:52) calculator program
                double num1 = 10;
                double num2 = 5;
                string op = "+";
                switch(op) {
                    case "+": Console.WriteLine(num1 + num2); break;
                    case "-": Console.WriteLine(num1 - num2); break;
                }
            }

            // ==========================================
            // #21 (01:46:53) arrays
            // Python: list = ["A", "B"] (Dynamic size)
            // C# Arrays have a FIXED size. You cannot append later.
            string[] cars = { "BMW", "Mustang", "Corvette" };
            cars[0] = "Tesla"; 

            // ==========================================
            // #22 (01:52:50) foreach loop
            // Python: for car in cars:
            foreach (string car in cars) {
                Console.WriteLine(car);
            }

            // ==========================================
            // EXECUTION OF METHODS (#23 - #26)
            // ==========================================
            SingHappyBirthday("Bro", 21);
            
            double mySquare = Square(5); // Returns 25
            double myVolume = Multiply(5, 4, 3); // Overloaded method
            
            double cartTotal = CheckOut(3.99, 5.75, 15); // Params method
            

            // ==========================================
            // #27 (02:08:52) exception handling
            // Python: try/except/finally
            try {
                int z = 10 / Convert.ToInt32("0"); // Forces an error
            }
            catch (DivideByZeroException) {
                Console.WriteLine("Math broke!");
            }
            catch (Exception) {
                Console.WriteLine("General error caught!");
            }
            finally {
                Console.WriteLine("This always runs.");
            }

            // ==========================================
            // #28 (02:13:53) conditional operator
            // Python: status = "Adult" if age >= 18 else "Minor"
            int myAge = 20;
            string status = (myAge >= 18) ? "Adult" : "Minor";

            // ==========================================
            // #29 (02:16:53) string interpolation
            // Python: f"Hello {name}"
            Console.WriteLine($"Hello {name}, your status is {status}");

            // ==========================================
            // #30 (02:20:18) multidimensional arrays
            // Python: grid = [[1, 2], [3, 4]]
            string[,] grid = { 
                { "A", "B", "C" }, 
                { "D", "E", "F" } 
            };
            Console.WriteLine(grid[0, 1]); // Prints "B"

        } // <--- END OF MAIN METHOD

        // ==========================================
        // METHOD BLUEPRINTS (#23 - #26)
        // Must be declared outside of Main, inside the Class.
        // ==========================================

        // #23 (01:54:42) methods
        // Python: def sing_happy_birthday(name, age):
        // 'void' means it does not return a value.
        static void SingHappyBirthday(string name, int age) 
        {
            Console.WriteLine($"Happy birthday {name}, age {age}!");
        }

        // #24 (02:00:37) return keyword
        // Replace 'void' with the data type you are returning (double).
        static double Square(double number) 
        {
            return number * number;
        }

        // #25 (02:04:12) method overloading
        // C# allows multiple methods with the exact same name, as long as the inputs are different.
        static double Multiply(double x, double y) {
            return x * y;
        }
        static double Multiply(double x, double y, double z) {
            return x * y * z;
        }

        // #26 (02:05:44) params keyword
        // Python: *args
        // Allows you to pass a comma-separated list of arguments without manually building an array first.
        static double CheckOut(params double[] prices) 
        {
            double total = 0;
            foreach (double price in prices) {
                total += price;
            }
            return total;
        }

    } // <--- END OF CLASS
} // <--- END OF NAMESPACE