namespace Interface_Segregation_Principle;

public class Sphere : IShape3D
{
    public double radius;
    
    public Sphere(double radius)
    {
        this.radius = radius;
    }
    
    public double Area()
    {
        return  Math.PI * Math.Pow(radius, 2);
    }

    public double Volume()
    {
        return Math.PI * Math.Pow(radius, 3) * 4/3;
    }
}