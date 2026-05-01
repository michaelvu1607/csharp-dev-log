// Dependency Inversion Principle (DIP)
// High-level modules should not depend on low-level modules. Both should depend on abstractions.

using Dependency_Inversion_Principle;

Car car = new Car(new ElectricEngine());
car.StartCar();