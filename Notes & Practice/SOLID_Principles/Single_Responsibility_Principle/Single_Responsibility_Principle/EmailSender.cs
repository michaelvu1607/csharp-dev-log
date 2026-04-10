namespace Single_Responsibility_Principle;

// solely handles sending emails

public class EmailSender
{
    public void SendEmail(string email, string message)
    {
        Console.WriteLine($"Sending email to {email}:  {message}");
    }
}