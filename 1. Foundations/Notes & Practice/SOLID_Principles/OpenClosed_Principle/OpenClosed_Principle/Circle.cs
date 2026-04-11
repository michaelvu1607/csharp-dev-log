namespace OpenClosed_Principle;

public class Circle : Shape
{
    public double Radius { get; set; }
    
    public override double Area()
    {
        return Math.PI * Math.Pow(Radius, 2);
    }

}