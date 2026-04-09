using System;
using System.Collections.Generic;

namespace ArchitecturalCheatSheet
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("System Architecture Initialized.");
            // Most design pattern logic runs automatically through how objects 
            // interact, rather than standard top-down execution here.
        }
    }

    // ==========================================
    // LEVEL 1: THE FOUNDATIONS 
    // [WATCH/LEARN: Phase 1, Weeks 3-4]
    // ==========================================

    // (0:12:19) OOP Concepts & (0:12:42) Encapsulation
    // Hide the internal state. Only expose what is safe to change.
    public class MotorController
    {
        private double voltage; // Hidden from outside interference

        public void SetVoltage(double v)
        {
            if (v >= 0 && v <= 12.0) // Safe access
                voltage = v;
        }
    }

    // (0:45:04) Coupling & (0:55:17) Composition vs Inheritance
    // (1:01:00) Fragile Base Class Problem
    // INHERITANCE (High Coupling - Avoid if possible): 
    // class FlyingRobot : Robot { ... } 
    // COMPOSITION (Low Coupling - Unity's default approach):
    // Give a standard Robot a "FlyingComponent" instead.
    public class Robot
    {
        // The Robot "has a" motor, it doesn't inherit from one.
        private MotorController _motor = new MotorController(); 
        
        public void Move()
        {
            _motor.SetVoltage(5.0);
        }
    }

    // ==========================================
    // LEVEL 2: S.O.L.I.D. PRINCIPLES
    // [WATCH/LEARN: Phase 1, Weeks 3-4]
    // ==========================================

    // (1:15:01) S - Single Responsibility Principle
    // A class should do ONE thing.
    public class NavigationSystem { /* Only calculates routes */ }
    public class BatteryMonitor   { /* Only checks power */ }

    // (1:21:26) O - Open/Closed Principle
    // Open for extension, closed for modification. 
    // You can add new behaviors without rewriting existing, tested code.
    public abstract class Sensor 
    {
        public abstract void Scan();
    }
    // We can add a LidarSensor later without ever touching the CameraSensor code.
    public class CameraSensor : Sensor { public override void Scan() { } }
    public class LidarSensor : Sensor  { public override void Scan() { } }

    // (1:45:20) I - Interface Segregation
    // Don't force classes to implement methods they don't need.
    // Bad: IEntity { void Move(); void Fly(); void Swim(); }
    // Good: Break it up!
    public interface IMovable { void Move(); }
    public interface IFlyable { void Fly(); }

    // (1:54:10) D - Dependency Inversion
    // High-level modules should depend on abstractions (interfaces), not concrete classes.
    public class Drone
    {
        private IMovable _movementLogic; // Depends on the interface, not a specific engine type

        public Drone(IMovable movementLogic) 
        {
            _movementLogic = movementLogic;
        }
    }

    // ==========================================
    // LEVEL 3: ESSENTIAL DESIGN PATTERNS
    // ==========================================

    // (2:33:40) STATE PATTERN
    // [WATCH/LEARN: Phase 1, Weeks 5-6 (The Drone State Machine Drill)]
    // Allows an object to completely change its behavior when its internal state changes.
    public interface IDroneState
    {
        void Handle(DroneContext context);
    }

    public class TakeoffState : IDroneState
    {
        public void Handle(DroneContext context)
        {
            Console.WriteLine("Taking off. Transitioning to Patrol State next.");
            // context.State = new PatrolState(); 
        }
    }

    public class DroneContext
    {
        public IDroneState CurrentState { get; set; }
        public void RequestAction() { CurrentState.Handle(this); }
    }


    // (4:56:50) OBSERVER PATTERN
    // [WATCH/LEARN: Phase 2, Weeks 11-12 (Unity Event Physics Puzzle)]
    // One object broadcasts an event; multiple independent objects listen and react.
    public class Target
    {
        // C# uses the 'event' and 'Action' keywords natively for the Observer pattern
        public event Action OnTargetHit; 

        public void TakeDamage()
        {
            // If anything is listening, shout that we got hit!
            OnTargetHit?.Invoke(); 
        }
    }

    public class ScoreUI
    {
        public void UpdateScore() { Console.WriteLine("Score increased!"); }
    }


    // (7:56:09) ADAPTER PATTERN
    // [WATCH/LEARN: Phase 4 (Integration phase)]
    // Wraps incompatible code so it works with your system.
    // Example: Taking a Python OpenCV script's output and making it readable to C#.
    public interface IUnityVision 
    { 
        double[] GetCoordinates(); 
    }

    public class PythonOpenCVLibrary 
    { 
        public string GetRawJSON() { return "[10.5, 20.1]"; } 
    }

    public class VisionAdapter : IUnityVision
    {
        private PythonOpenCVLibrary _pythonLib = new PythonOpenCVLibrary();

        public double[] GetCoordinates()
        {
            // Translates the Python string into the C# double array Unity needs
            string raw = _pythonLib.GetRawJSON();
            return new double[] { 10.5, 20.1 }; 
        }
    }


    // (10:19:13) SINGLETON PATTERN
    // [WATCH/LEARN: Phase 1, Weeks 5-6 (System Diagnostics)]
    // Ensures a class has only ONE instance globally. Perfect for a central logger.
    public class DiagnosticsLogger
    {
        private static DiagnosticsLogger _instance;

        // Private constructor prevents anyone else from making one
        private DiagnosticsLogger() { } 

        public static DiagnosticsLogger Instance
        {
            get
            {
                if (_instance == null)
                    _instance = new DiagnosticsLogger();
                return _instance;
            }
        }

        public void Log(string message) { Console.WriteLine(message); }
    }

    // ==========================================
    // INDUSTRY TOOLS
    // [WATCH/LEARN: Phase 1, Weeks 1-2]
    // ==========================================
    // (1:05:24) UML
    // Not code! This is the planning stage before you write C#.
    // You will sketch out boxes with lines connecting them to plan your classes
    // before touching the keyboard.
}