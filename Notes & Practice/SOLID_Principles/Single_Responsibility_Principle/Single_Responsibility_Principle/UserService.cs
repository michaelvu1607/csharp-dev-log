namespace Single_Responsibility_Principle;

// UserService class solely handles user registration

public class UserService
{
    public void Register(User user)
    {
        EmailSender emailSender = new  EmailSender();
        emailSender.SendEmail(user.Email,"Welcome to Our Platform");
    }
}