namespace Encapsulation;

public class SmartWallet 
{
    // 1. HIDDEN DATA: No one can see or touch this directly
    private decimal _cash; 

    // 2. CONTROLLED ACCESS: People can check the balance, but not change it
    public decimal Cash => _cash; 

    // 3. SECURE METHODS: The only way to modify data is through logic
    public void Deposit(decimal amount) 
    {
        if (amount > 0) 
        {
            _cash += amount;
            Console.WriteLine($"Deposited: {amount}");
        }
    }

    public bool Withdraw(decimal amount) 
    {
        if (amount <= _cash) 
        {
            _cash -= amount;
            return true;
        }
        Console.WriteLine("Insufficient funds!");
        return false;
    }
}