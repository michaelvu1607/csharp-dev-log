namespace IInteractable;

public class BlastDoor : IInteractable
{
    private bool _doorState;
    private readonly IUnlock _unlock1;
    private readonly IUnlock _unlock2;

    public BlastDoor(IUnlock unlock1, IUnlock unlock2)
    {
        _unlock1 = unlock1;
        _unlock2 = unlock2;
    }

    private bool Openable()
    {
        if (_unlock1.Toggle && _unlock2.Toggle)
        {
            return true;
        }
        return false;

    }

    public void Interact()
    {
        if (Openable())
        {
            Console.WriteLine("Opening door...");
            _doorState = true;
        }
        else
        {
            Console.WriteLine("Door cannot be opened.");
            _doorState = false;
        }
    }
    
    public override string ToString()
    {
        if (_doorState)
        {
            return "Door is Open";
        }
        return "Door is Closed";
    }
}