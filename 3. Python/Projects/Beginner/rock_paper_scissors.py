import random

user_wins = 0
computer_wins = 0

options = ["rock", "paper", "scissors"]

while True:
    user_input = input("Rock Paper Scissors (Q to quit): ").lower()
    if user_input == "q":
        break

    if user_input not in options:
        print("Please enter a rock, paper, or scissors.")
        continue

    random_number = random.randint(0, 2)
    # rock: 0 | paper: 1 | scissors: 2
    computer_pick = options[random_number]
    print(f"Computer picks {computer_pick}")

    if user_input == "rock" and computer_pick == "scissors":
        print("You win!")
        user_wins += 1
    elif user_input == "rock" and computer_pick == "paper":
        print("You lose!")
        computer_wins += 1

    elif user_input == "paper" and computer_pick == "rock":
        print("You win!")
        user_wins += 1
    elif user_input == "paper" and computer_pick == "scissors":
        print("You lose!")
        computer_wins += 1

    elif user_input == "scissors" and computer_pick == "paper":
        print("You win!")
        user_wins += 1
    elif user_input == "scissors" and computer_pick == "rock":
        print("You lose!")
        computer_wins += 1

    else:
        print("Tie!")

    print(f"Score: {user_wins} | {computer_wins}")
print("Good bye!")