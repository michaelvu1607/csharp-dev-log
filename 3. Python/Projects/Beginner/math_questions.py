#still buggy but i dont feel like fixing it

import random
import time

OPERATORS = ["+", "-", "*"]
MIN_VALUE = 2
MAX_VALUE = 12
TOTAL_PROBLEMS = 5

def generate_problem():
    left = random.randint(MIN_VALUE, MAX_VALUE)
    right = random.randint(MIN_VALUE, MAX_VALUE)
    operator = random.choice(OPERATORS)
    expr = f"{str(left)} {operator} {str(right)}"
    answer = eval(expr)
    return expr, answer

def set_questions():
    number_wrong = 0
    number_right = 0
    for i in range(TOTAL_PROBLEMS):
        expr, answer = generate_problem()
        guess = input(f"Problem # {i + 1}: {expr} = ")
        while True:
            if guess.isdigit() or (guess.startswith("-") and guess[1:].isdigit()):
                if guess == str(answer):
                    print("Correct! ")
                    number_right += 1
                    break
                else:
                    print("Incorrect. Try again. ")
                    guess = input("= ")
                    number_wrong += 1
                    continue
            else:
                print("Must be a whole number. Try again. ")
                guess = input("= ")
                continue
    return number_wrong, number_right

def unlimited_questions():
    start_time = time.time()
    number_wrong = 0
    number_right = 0
    question_number = 0
    a = 1
    while a == 1:
        question_number += 1
        expr, answer = generate_problem()
        guess = input(f"Problem # {question_number}: {expr} = ")
        while True:
            if guess.lower() == "q":
                a = -1
                number_wrong -= 1
                number_right -= 1
                break
            elif guess.isdigit() or (guess.startswith("-") and guess[1:].isdigit()):
                if guess == str(answer):
                    print("Correct! ")
                    number_right += 1
                    break
                else:
                    print("Incorrect. Try again. ")
                    guess = input("= ")
                    number_wrong += 1
                    continue
            else:
                print("Must be a whole number. Try again. ")
                guess = input("= ")
                continue

    end_time = time.time()
    total_time = end_time - start_time
    average_time = average_time = total_time / question_number
    return total_time, average_time, question_number

def main():
    mode = input("Select a mode: Timer or Limited: ").lower()

    while True:
        if mode == "timer":
            print("Type Q to quit")
            input("Press enter to start. ")
            print("-------------------------)")

            total_time, average_time, question_number = unlimited_questions()
            print(f"It took you {round(total_time, 2)} seconds to answer {question_number} questions which is an average of {round(average_time, 2)} seconds per question")
            print("-----------------------------------")
            break
        elif mode == "limited":
            input("Press enter to start. ")
            print("-------------------------)")
            number_wrong, number_right = set_questions()
            print(f"Your total score is: {number_right}/{number_wrong + number_right} or {number_right / (number_wrong + number_right) * 100}%. ")
            print("-----------------------------------")
            break
        else:
            print("Not an option. Try Again. ")
            mode = input("Timer or Limited: ").lower()
            continue

main()