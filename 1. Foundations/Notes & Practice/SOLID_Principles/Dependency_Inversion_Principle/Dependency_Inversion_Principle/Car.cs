namespace Dependency_Inversion_Principle;

public class Car
{
    private IEngine _engine;

    public Car(IEngine engine)
    {
        _engine = engine;
    }

    public void StartCar()
    {
        _engine.Start();
        Console.WriteLine("Car Started");
    }
}