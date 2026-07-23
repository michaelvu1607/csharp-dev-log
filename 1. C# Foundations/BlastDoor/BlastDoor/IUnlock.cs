namespace IInteractable;

public interface IUnlock
{
    bool Toggle { get; }
    bool ChangeLockedState();
}