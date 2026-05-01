namespace Dependency_Inversion_Principle;

public class ElectricEngine : IEngine
{
    public void Start()
    {
        Console.WriteLine("Starting Electric Engine");
    }
}