namespace OpenClosed_Principle;

public class Triangle : Shape
{
    public double  Width { get; set; }
    public double Height { get; set; }

    public override double Area()
    {
        return Width * Height / 2;
    }
}