using prac;

BankAccount balance = new BankAccount(100);
Console.WriteLine(balance.GetBalance());

balance.Deposit(50);
Console.WriteLine(balance.GetBalance());

balance.Withdraw(100);
Console.WriteLine(balance.GetBalance());