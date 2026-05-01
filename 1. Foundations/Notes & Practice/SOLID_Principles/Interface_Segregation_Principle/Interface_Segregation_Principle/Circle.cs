namespace Interface_Segregation_Principle;

public class Circle : IShape2D
{
    public double radius;
    
    public Circle(double radius)
    {
        this.radius = radius;
    }
    
    public double Area()
    {
        return  Math.PI * Math.Pow(radius, 2);
    }
}