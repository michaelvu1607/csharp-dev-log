using System;

namespace SystemDiagnostics
{
   // TASK 1: Define your 'Vector3' struct here. 
   // Use 'readonly', 'init', and the '(X, Y, Z) = (x, y, z)' shortcut.
   public readonly struct Vector3
   {
      public double X { get; init; }
      public double Y { get; init; }
      public double Z { get; init; }
      
      public Vector3(double x, double y, double z) => (X, Y, Z) = (x, y, z);
      // Inside the Vector3 struct
      public override string ToString() => $"({X}, {Y}, {Z})";
      
   }

   public class Robot
   {
      public string Name { get; set; }
      public Vector3 CurrentPosition { get; set; }

      public Robot(string name, Vector3 startPos)
      {
         // TASK 2: Initialize the robot's name and position here.
         this.Name = name;
         this.CurrentPosition = startPos;
      }

      // TASK 3: Create a method that takes a 'Vector3 target' 
      // and returns a 'double' (the distance).
      public double CalculateDistance(Vector3 target)
      {
         // 1. Find the difference (delta) for each axis
         double deltaX = target.X - this.CurrentPosition.X;
         double deltaY = target.Y - this.CurrentPosition.Y;
         double deltaZ = target.Z - this.CurrentPosition.Z;

         // 2. Square the differences and add them up
         double sumOfSquares = Math.Pow(deltaX, 2) + Math.Pow(deltaY, 2) + Math.Pow(deltaZ, 2);

         // 3. Return the square root of that sum
         return Math.Sqrt(sumOfSquares);
      }
   }

   class StructsProgram
   {
      static void Main(string[] args)
      {
         // TASK 4: In Main, create a Robot at (0,0,0).
         // Then, calculate the distance to a target at (10, 5, 8).

         Vector3 startPos = new Vector3(0, 0, 0);
         Robot robot = new Robot("Bob", startPos);

         bool running = true;
         while (running)
         {
            Console.Write("Enter an x coordinate: ");
            string lineX = Console.ReadLine();
            Console.Write("Enter an y coordinate: ");
            string lineY = Console.ReadLine();
            Console.Write("Enter an z coordinate: ");
            string lineZ = Console.ReadLine();
            if (double.TryParse(lineX, out double x) && double.TryParse(lineY, out double y) &&
                double.TryParse(lineZ, out double z))
            {
               Vector3 endPos = new Vector3(x, y, z);
               Console.WriteLine(robot.CalculateDistance(endPos));
               Console.WriteLine($"{startPos} -> {endPos}");
            }
            else
            {
               Console.WriteLine("Invalid input. Please enter numerical values.");
            }

            bool invalidInput;
            do
            {
               invalidInput = false;
               Console.Write("Check Another (y/n)?: ");
               string answer = Console.ReadLine()?.ToLower();
               
               if (answer == "n")
               {
                  running = false;
               }
               else if (answer != "y")
               {
                  Console.WriteLine("Invalid input. Please enter 'y' or 'n'.");
                  invalidInput = true;
               }
               
            } 
            while (invalidInput) ;
         }
         Console.WriteLine("Diagnostics complete. Press any key to exit...");
         Console.ReadKey();
      }
   }
}