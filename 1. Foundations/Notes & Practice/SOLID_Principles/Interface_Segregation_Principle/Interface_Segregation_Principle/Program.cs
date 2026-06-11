// Interface Segregation Principle (ISP)
// Clients should not be forced to depend on interfaces they do not use.

using Interface_Segregation_Principle;

Circle circle = new Circle(5);
Console.WriteLine(circle.Area());

Sphere sphere = new Sphere(3);
Console.WriteLine(sphere.Area());
Console.WriteLine(sphere.Volume());
