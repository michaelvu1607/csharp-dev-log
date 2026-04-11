// Single Responsibility Principle (SRP)
// A class should have only one reason to change, meaning that it should have only one responsibility or purpose

using Single_Responsibility_Principle;

User user = new User();
user.Email = "michaelvu1607@gmail.com";
user.Username = "Michael Vu";

UserService userService = new UserService();
userService.Register(user);