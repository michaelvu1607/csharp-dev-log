namespace prac;
//Encapsulation
public class BankAccount
{
    private decimal _balance;

    public BankAccount(decimal balance)
    {
        Deposit(balance);
    }
    
    public decimal GetBalance()
    {
        return _balance;
    }

    public void Deposit(decimal amount)
    {
        if (amount <= 0)
        {
            throw new ArgumentException("amount must be greater than zero");
        }
        _balance += amount;
    }

    public void Withdraw(decimal amount)
    {
        if (amount <= 0)
        {
            throw new ArgumentException("amount must be greater than zero");
        }

        if (amount > _balance)
        {
            throw new InvalidOperationException("Insufficient balance");
        }
        _balance -= amount;
    }
}