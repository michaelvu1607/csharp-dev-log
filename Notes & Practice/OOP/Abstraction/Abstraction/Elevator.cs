namespace Abstraction;
// ABSTRACTION: This defines WHAT an elevator does, not HOW.
public abstract class Elevator 
{
    // Essential data everyone needs to see
    public int CurrentFloor { get; protected set; }

    // The "Interface": The only things the user needs to know
    public abstract void GoToFloor(int floor);
    public abstract void OpenDoors();
}