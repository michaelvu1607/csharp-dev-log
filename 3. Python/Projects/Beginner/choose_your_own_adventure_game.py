name = input("What's your name? ").title()
print(f"Welcome {name} to your adventure!")

answer = input("You are on a dirt road. A crossroad appears ahead. You can go left or right.\nWhich way would you like to go? ").lower()

if answer == "left":
    answer = input("You come to a river. You can swim across or walk around it. Type \"swim\" to swim across or type \"walk\" to walk around it.\nWhich way would you like to go? ").lower()
    if answer == "walk":
        print("You walked and ran out of water and died")
    elif answer == "swim":
        print("You swam across and got hypothermia and died.")
    else:
        print("Not a valid option. You died.")

elif answer == "right":
    answer = input("You come to a wobbly bridge.\nDo you want to cross or go back? [cross/back] " ).lower()
    if answer == "back":
        print("You go back and ran out of water and died")
    elif answer == "cross":
        answer = input("You cross a bridge and meet a stranger.\nDo you talk to them [yes/no] ").lower()
        if answer == "yes":
            print(f"You talk to the stranger and they give you gold.\nCONGRATULATIONS, {name}, YOU WIN!!!")
        elif answer == "no":
            print("You fall off a cliff and die.")
        else:
            print("Not a valid option. You died.")

    else:
        print("Not a valid option. You died.")
else:
    print("Not a valid option. You died.")