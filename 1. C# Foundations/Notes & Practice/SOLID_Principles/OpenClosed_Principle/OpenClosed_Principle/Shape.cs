namespace OpenClosed_Principle;

// classes of shapes inherit from this class
// each class responsible for its own properties and calculating its own Area
// adding new shape -> extends coverage of shapes but doesn't modify any previous shape class

public abstract class Shape
{
    public abstract double Area();
}