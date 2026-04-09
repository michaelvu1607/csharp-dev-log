namespace IInteractable;

public class Switch : IUnlock
{
    public bool Toggle { get; private set; }

    public bool ChangeLockedState()
    {
        Toggle = !Toggle;

        if (Toggle)
        {
            Console.WriteLine("Switched On");
            return true;
        }
        Console.WriteLine("Switched Off");
        return false;
    }

    public override string ToString()
    {
        if (Toggle)
        {
            return "Switched On";
        }
        return "Switched Off";
    }
}