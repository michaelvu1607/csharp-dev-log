import random

top_of_range = input("Type a number: ")
if top_of_range.isdigit():
    top_of_range = int(top_of_range)
    if top_of_range <= 0:
        print("Please enter a number greater than 0 next time.")
        quit()
else:
    print("Please enter a number next time.")
    quit()

random_number = random.randint(1,top_of_range)

number_of_guesses = 0

print(f"Guess a number from 1 to {top_of_range}: ")

while True:
    guess = input("")

    if guess.isdigit():
        guess = int(guess)
        number_of_guesses += 1
        if guess <= 0:
            print("Please enter a number greater than 0.")
            continue
    else:
        print("Please enter a number.")
        continue
    if guess == random_number:
        break
    elif guess > random_number:
        print("The Number is Lower")
    else:
        print("The Number is Higher")

print(f"Congratulations! You have guessed the number {random_number}.")
print(f"It took you {number_of_guesses} guesses.")