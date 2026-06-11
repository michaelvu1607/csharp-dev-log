namespace IInteractable;

public class Key : IUnlock
{
    public bool Toggle { get; private set; }

    public bool ChangeLockedState()
    {
        Toggle = !Toggle;

        if (Toggle)
        {
            Console.WriteLine("Unlocking with key...");
            return true;
        }
        Console.WriteLine("Locking with key...");
        return false;
    }
    
    public override string ToString()
    {
        if (Toggle)
        {
            return "Door is Unlocked";
        }
        return "Door is Locked";
    }
}