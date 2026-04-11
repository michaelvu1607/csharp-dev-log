namespace Inheritance;

public abstract class Unit
{
    public string Name { get; set; }
    
    // Constructor using 'base'
    public Unit(string name) => Name = name;

    // Abstract: Force child to define this
    public abstract void Process();

    // Virtual: Optional to change
    public virtual void Alert() => Console.WriteLine("Alert!");
}