using System;
using System.Collections.Generic; // Required for #44 and #45 (Lists)
using System.Threading;           // Required for #50 (Multithreading)

namespace BroCodeOOPCheatSheet
{
    class Program
    {
        static void Main(string[] args)
        {
            // ==========================================
            // #31 CLASSES & #32 OBJECTS
            // ==========================================
            // Python: class Robot: ... my_robot = Robot()
            // C#: Requires the 'new' keyword to instantiate an object from a class blueprint.
            Robot robot1 = new Robot("Alpha");
            robot1.Introduce();

            // ==========================================
            // #33 CONSTRUCTORS
            // ==========================================
            // Python: def __init__(self, name):
            // The constructor is called automatically when 'new' is used above.
            
            // ==========================================
            // #34 STATIC
            // ==========================================
            // Python: Class attributes (Robot.population)
            // Static members belong to the class itself, not any individual object.
            Console.WriteLine($"Total Robots created: {Robot.robotCount}");

            // ==========================================
            // #35 OVERLOADED CONSTRUCTORS
            // ==========================================
            // C# allows multiple constructors with different parameters. 
            // Python usually handles this with default arguments (color=None).
            Robot robot2 = new Robot("Beta", "Red");

            // ==========================================
            // #38 ARRAY OF OBJECTS
            // ==========================================
            // C# arrays have a fixed size.
            Robot[] squad = new Robot[2];
            squad[0] = robot1;
            squad[1] = robot2;

            // ==========================================
            // #39 OBJECTS AS ARGUMENTS
            // ==========================================
            // Passing a specific object instance into a method.
            RepairRobot(robot1);

            // ==========================================
            // #40 METHOD OVERRIDING & #36 INHERITANCE
            // ==========================================
            // Python handles overrides implicitly. C# requires 'virtual' in the parent and 'override' in the child.
            Drone myDrone = new Drone("Scout");
            myDrone.Move(); // Calls the overridden method in the Drone class

            // ==========================================
            // #41 TOSTRING METHOD
            // ==========================================
            // Python: def __str__(self):
            // Overriding the default string representation of an object.
            Console.WriteLine(myDrone.ToString());

            // ==========================================
            // #42 POLYMORPHISM
            // ==========================================
            // Greek for "many forms". Objects of different classes can be treated as the same parent type.
            Vehicle[] vehicles = { new Rover(), new Drone("Delivery") };
            foreach (Vehicle v in vehicles)
            {
                v.Move(); // C# automatically knows which specific Move() to call
            }

            // ==========================================
            // #43 INTERFACES
            // ==========================================
            // A contract that enforces classes to implement specific methods.
            // Python uses Abstract Base Classes (abc) for this.
            Sensor arraySensor = new Sensor();
            arraySensor.Ping();

            // ==========================================
            // #44 LISTS & #45 LIST OF OBJECTS
            // ==========================================
            // Python: my_list = []
            // C# Lists are dynamic in size but strictly typed using Generics <T>.
            List<Robot> activeRoster = new List<Robot>();
            activeRoster.Add(robot1);
            activeRoster.Add(new Robot("Gamma"));

            foreach (Robot r in activeRoster)
            {
                Console.WriteLine(r.name);
            }

            // ==========================================
            // #48 ENUMS
            // ==========================================
            // Python: from enum import Enum
            // A special "class" that represents a group of constants.
            SystemState currentState = SystemState.Booting;
            if (currentState == SystemState.Booting)
            {
                Console.WriteLine($"System is currently {(int)currentState} (Booting)");
            }

            // ==========================================
            // #49 GENERICS
            // ==========================================
            // Allows methods/classes to work with any data type.
            double[] coordinates = { 10.5, 20.2, 5.1 };
            string[] logs = { "Boot", "Scan", "Idle" };
            
            DisplayData(coordinates);
            DisplayData(logs);

            // ==========================================
            // #50 MULTITHREADING
            // ==========================================
            // Python: import threading
            // Executing multiple execution paths simultaneously.
            Thread sensorThread = new Thread(RunSensors);
            sensorThread.Start();
            
            Console.WriteLine("Main program continuing while sensors run in background...");

        } // <--- END OF MAIN METHOD

        // ==========================================
        // METHODS FOR MAIN
        // ==========================================

        // #39 Objects as arguments
        static void RepairRobot(Robot r)
        {
            r.BatteryLevel = 100; // Uses the Setter (#46)
            Console.WriteLine($"{r.name} has been fully repaired.");
        }

        // #49 Generics (<T>)
        static void DisplayData<T>(T[] array)
        {
            foreach (T item in array)
            {
                Console.Write($"{item} ");
            }
            Console.WriteLine();
        }

        // #50 Multithreading method
        static void RunSensors()
        {
            Console.WriteLine("[Thread 2] Sensors starting...");
            Thread.Sleep(1500); // Pause this thread for 1.5 seconds
            Console.WriteLine("[Thread 2] Sensors online.");
        }
    }

    // ==========================================
    // OOP BLUEPRINTS (CLASSES, INTERFACES, ENUMS)
    // ==========================================

    // #37 ABSTRACT CLASSES
    // Python: class Vehicle(ABC):
    // Cannot be instantiated directly (no 'new Vehicle()'). Must be inherited.
    abstract class Vehicle
    {
        public abstract void Move(); // Incomplete method; child MUST finish it
    }

    class Rover : Vehicle
    {
        public override void Move()
        {
            Console.WriteLine("Rover is driving on wheels.");
        }
    }

    // #31 CLASSES
    class Robot
    {
        // #34 STATIC
        // Belongs to the class, shared by all objects.
        public static int robotCount = 0;

        public string name;
        public string color;

        // #46 GETTERS & SETTERS
        // Python: @property
        private int _batteryLevel;
        public int BatteryLevel
        {
            get { return _batteryLevel; }
            set 
            { 
                if (value >= 0 && value <= 100) 
                {
                    _batteryLevel = value; 
                }
            }
        }

        // #47 AUTO IMPLEMENTED PROPERTIES
        // A shortcut when you don't need custom get/set logic.
        public string ModelID { get; set; }

        // #33 CONSTRUCTORS
        // Python: def __init__(self, name):
        public Robot(string name)
        {
            this.name = name;
            this.color = "Standard Gray";
            this.BatteryLevel = 100;
            robotCount++;
        }

        // #35 OVERLOADED CONSTRUCTORS
        // Same method name, different parameters.
        public Robot(string name, string color)
        {
            this.name = name;
            this.color = color;
            this.BatteryLevel = 100;
            robotCount++;
        }

        // Parent method marked 'virtual' so children can override it (#40)
        public virtual void Introduce()
        {
            Console.WriteLine($"Hello, I am {name}.");
        }
    }

    // #36 INHERITANCE
    // Drone inherits everything from Robot
    class Drone : Vehicle
    {
        public string name;

        public Drone(string name)
        {
            this.name = name;
        }

        // #40 METHOD OVERRIDING
        // Python overrides automatically. C# needs the 'override' keyword.
        public override void Move()
        {
            Console.WriteLine($"Drone {name} is flying through the air.");
        }

        // #41 TOSTRING METHOD
        public override string ToString()
        {
            return $"[This is a Drone named {name}]";
        }
    }

    // #43 INTERFACES
    // Defines rules that a class must follow.
    interface IScannable
    {
        void Ping();
    }

    // Class implementing an interface
    class Sensor : IScannable
    {
        public void Ping()
        {
            Console.WriteLine("Sensor pinging environment... Clear.");
        }
    }

    // #48 ENUMS
    // A strict list of numbered options. By default, Booting = 0, Idle = 1, etc.
    enum SystemState
    {
        Booting,
        Idle,
        Active,
        Error
    }
}