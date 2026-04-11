namespace IInteractable;

public class Terminal : IInteractable
{
    private readonly IUnlock _switch;
    private readonly IUnlock _key;
    private readonly IInteractable _door;

    public Terminal(IUnlock switch0, IUnlock key, IInteractable door)
    {
        _switch = switch0;
        _key = key;
        _door = door;
    }
    
    public void Interact()
    {
        Console.WriteLine("----------------------------");
        Console.WriteLine("Interacting with Terminal...");
        Console.WriteLine(_switch);
        Console.WriteLine(_key);
        Console.WriteLine(_door);
        Console.WriteLine("----------------------------");
    }
}