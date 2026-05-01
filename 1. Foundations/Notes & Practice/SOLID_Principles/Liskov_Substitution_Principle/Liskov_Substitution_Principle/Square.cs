namespace Liskov_Substitution_Principle;

public class Square : Shape
{
    public double SideLength { get; set; }
    
    public override double Area {  get => SideLength * SideLength; }
}