using System.Collections.Generic;
using Polymorphism;

// 1. UPCASTING: We create a list of the BASE type (Vehicle). 
// This allows us to group different objects (Car, Motorcycle, Plane) together 
// because they all "is-a" Vehicle.
List<Vehicle> vehicles = new List<Vehicle>();

vehicles.Add(new Car());
vehicles.Add(new Motorcycle());
vehicles.Add(new Plane());

// 2. THE POLYMORPHIC LOOP: We iterate through the list using the base reference.
foreach (var vehicle in vehicles)
{
    // 3. DYNAMIC POLYMORPHISM (Runtime Binding):
    // Even though 'vehicle' is typed as a Vehicle here, C# looks at the 
    // ACTUAL object type in memory. 
    
    // If it's a Car, it runs Car.Start(). 
    // If it's a Plane, it runs Plane.Start().
    
    // This allows one line of code to trigger many different behaviors.
    vehicle.Start();
}