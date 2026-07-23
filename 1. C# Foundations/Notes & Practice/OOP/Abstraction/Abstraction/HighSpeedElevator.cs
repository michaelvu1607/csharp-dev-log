namespace Abstraction;

// IMPLEMENTATION: The messy details are hidden inside specific classes.
public class HighSpeedElevator : Elevator 
{
    public override void GoToFloor(int floor) 
    {
        // Complex motor logic, acceleration curves, and safety checks happen here
        Console.WriteLine($"Accelerating quickly to floor {floor}...");
        CurrentFloor = floor;
    }

    public override void OpenDoors() => Console.WriteLine("Sliding doors open.");
}