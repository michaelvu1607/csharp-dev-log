using System;
using System.Collections.Generic;

namespace RobotFactory
{
    class RobotProgram
    {
        static void Main(string[] args)
        {
            Drone drone =  new Drone("Drone");
            Sentinel sentinel = new Sentinel("Sentinel");
        
            List<Robot> robots = new List<Robot>();
            robots.Add(drone);
            robots.Add(sentinel);

            foreach (Robot robot in robots)
            {
                robot.PerformanceTask();
            }

            foreach (Robot robot in robots)
            {
                if (robot is IFlyable)
                {
                    Console.WriteLine($"{robot} can fly");
                }
            }
            
            drone.UseBattery();
            Console.WriteLine(drone);
            drone.Charge();
            Console.WriteLine(drone);
            
            Console.ReadKey();
        }
    }

    interface IFlyable
    {
        void FlyingStatus();
    }

    abstract class Robot
    {
        protected string name;
        protected int battery;
        static Random rnd = new Random();

        public Robot(string name)
        {
            this.name = name;
            this.battery = rnd.Next(1, 101);
        }

        public abstract void PerformanceTask();

        public void UseBattery()
        {
            if (this.battery >= 15)
            {
                this.battery -= 15;
                Console.WriteLine("Using battery...");
            }
            else
            {
                Console.WriteLine($"Not enough battery: {this.battery}");
            }
        }

        public void Charge()
        {
            this.battery += rnd.Next(1, 51);
            if (this.battery > 100)
            {
                battery = 100;
            }

            Console.WriteLine("Charging...");
            Console.WriteLine($"{this.name} is now at {this.battery}%");
        }
        
        public override string ToString()
        {
            return $"Name: {name}, Battery %: {this.battery}" ;
        }
    }

    class Drone : Robot, IFlyable
    {
        public Drone(string name) : base(name)
        {
        }
        
        public void FlyingStatus()
        {
            Console.WriteLine("Flying");
        }

        public override void PerformanceTask()
        {
            FlyingStatus();
        }
    }

    class Sentinel : Robot
    {
        public Sentinel(string name) : base(name)
        {
        }

        public override void PerformanceTask()
        {
            Console.WriteLine("Scanning Perimeter");
        }
    }
}