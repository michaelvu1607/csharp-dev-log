// Liskov Substitution Principle (LSP)
// Objects of a superclass should be replaceable with objects of its subclass without affecting the correctness of the program

using Liskov_Substitution_Principle;

Shape rectangle = new Rectangle { Width = 5, Height = 4 };
Console.WriteLine($"Rectangle Area: {rectangle.Area}");

Shape square = new Square { SideLength = 5};
Console.WriteLine($"Rectangle Area: {square.Area}");
