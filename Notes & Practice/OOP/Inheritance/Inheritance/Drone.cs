namespace Inheritance;

public class Drone : Unit {
    public Drone(string name) : base(name) { } // Pass name to Unit

    public override void Process() => Console.WriteLine("Scanning...");

    public override void Alert() {
        base.Alert(); // Run original Alert
        Console.WriteLine("Drone Lights Flashing!");
    }
}