import random

vanguards = [
    "Angela",
    "Bruce Banner",
    "Captain America",
    "Doctor Strange",
    "Emma Frost",
    "Groot",
    "Magneto",
    "Namor",
    "Peni Parker",
    "Rogue",
    "The Thing",
    "Thor",
    "Venom"
]

duelists = [
    "Black Panther",
    "Black Widow",
    "Blade",
    "Daredevil",
    "Deadpool",
    "Elsa Bloodstone",
    "Hawkeye",
    "Hela",
    "Human Torch",
    "Iron Fist",
    "Iron Man",
    "Magik",
    "Mister Fantastic",
    "Moon Knight",
    "Phoenix",
    "Psylocke",
    "Scarlet Witch",
    "Spider-Man",
    "Squirrel Girl",
    "Star-Lord",
    "Storm",
    "The Punisher",
    "Winter Soldier",
    "Wolverine"
]

strategists = [
    "Adam Warlock",
    "Cloak & Dagger",
    "Gambit",
    "Invisible Woman",
    "Jeff the Land Shark",
    "Loki",
    "Luna Snow",
    "Mantis",
    "Rocket Raccoon",
    "Ultron"
]

character = ""

while True:
    role = input(f"Choose a role (V/D/S/q): ").lower()
    if role == "v":
        character = random.choice(vanguards)
        vanguards.remove(character)
    elif role == "d":
        character = random.choice(duelists)
        duelists.remove(character)
    elif role == "s":
        character = random.choice(strategists)
        strategists.remove(character)
    elif role == "q":
        break
    else:
        print("Not an option. Try again.")

    print(character)

