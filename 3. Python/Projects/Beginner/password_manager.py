'''doesn't work!!!'''


from cryptography.fernet import Fernet

'''
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)'''

def read_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key

master_pwd = input("What is the master password? ")
key = read_key() + master_pwd.encode()
fernet = Fernet(key)

def add():
    name = input("Account name: ")
    pwd = input("Password: ")

    with open("accounts.txt", "a") as f:
        f.write(f"{name} {(fernet.encrypt(pwd.encode()).decode())}\n")

def view():
    with open("accounts.txt", "r") as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split(" ")
            print(f"USERNAME: {user} | PASSWORD: {(fernet.decrypt(passw.encode()).decode())}")

while True:
    mode = input("Would you like to add a new password or view existing password?\n[add, view] or press Q to quit: ").lower()
    if mode == "add":
        add()
    elif mode == "view":
        view()
    elif mode == "q":
        quit()
    else:
        continue