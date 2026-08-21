import fetch_data
import trip_scoring

def prompt_user():
    answer = input("Choose an option:\n1. Search for Trips Directly\n2. Search for Trip Recommendations\n3. View Trip Recommendations\n[1-3]: ")
    return answer

def main():
    answer = prompt_user()
    while answer != "0":
        if answer == "1":
            fetch_data.search()
        elif answer == "2":
            trip_scoring.query()
        elif answer == "3":
            pass
        else:
            print("Not an option")
        answer = prompt_user()


if __name__ == "__main__":
    main()