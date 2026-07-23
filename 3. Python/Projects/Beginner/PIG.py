import random

MAX_SCORE = 25

def roll_dice():
    min_value = 1
    max_value = 6
    roll = random.randint(min_value, max_value)
    return roll

while True:
    players = input("How many players? [2-4]\n")
    if players.isdigit():
        players = int(players)
        if 2 <= players <= 4:
            break
        else:
            print("Must be between 2-4 players. ")
    else:
        print("Must be a number 2-4")

player_scores = [0 for _ in range(players)]
while max(player_scores) < MAX_SCORE:
    for player_idx in range(players):
        print(f"It's now player {player_idx + 1}'s turn. ")
        while True:
            should_roll = input("Would you like to roll? [y/n]\n").lower()
            if should_roll == "y":
                value = roll_dice()
                if value == 1:
                    print("You rolled a 1. Your score is now 0. Turn over!\n")
                    player_scores[player_idx] = 0
                    break
                else:
                    player_scores[player_idx] += value
                    print(f"You rolled a {value}. Your score is now {player_scores[player_idx]}!\n")
                    print(player_scores)
                    if player_scores[player_idx] >= MAX_SCORE:
                        print("Game Over!")
                        print(f"Player {player_scores.index(player_idx)} wins!")
                        quit()
            elif should_roll == "n":
                break
            else:
                print("Not a valid option. Try again.\n")
