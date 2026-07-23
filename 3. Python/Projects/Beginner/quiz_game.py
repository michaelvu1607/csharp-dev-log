response = input("Do you want to play a game? (type yes to continue) ")
if response.lower() != "yes":
    quit()

print("Welcome to the computer quiz game")
score = 0
question_number = 0

answer = input("What does CPU stand for? ")
if answer.lower() == "central processing unit":
    print("Correct!")
    score += 1
else:
    print("Incorrect")
question_number += 1
print(f"Score: {score} / {question_number}")

answer = input("What does GPU stand for? ")
if answer.lower() == "graphics processing unit":
    print("Correct!")
    score += 1
else:
    print("Incorrect")
question_number += 1
print(f"Score: {score} / {question_number}")

answer = input("What does RAM stand for? ")
if answer.lower() == "random access memory":
    print("Correct!")
    score += 1
else:
    print("Incorrect")
question_number += 1
print(f"Score: {score} / {question_number}")

if score == 3:
    print("Congratulations!")
elif score == 2:
    print("Not Bad!")
elif score == 1:
    print("Better Luck Next Time!")
elif score == 0:
    print("You Suck!")
percentage = score / question_number * 100
print(f"You had an accuracy of {percentage}%.")