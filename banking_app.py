# banking_app.py

accounts = {}  # username -> {"password": str, "balance": float}

def create_account():
    print("\n--- Create Account ---")
    username = input("Choose a username: ").strip()

    if username in accounts:
        print("That username already exists.\n")
        return

    password = input("Choose a password: ").strip()
    accounts[username] = {"password": password, "balance": 0.0}
    print("Account created!\n")

def login():
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username not in accounts or accounts[username]["password"] != password:
        print("Wrong username or password.\n")
        return None

    print(f"Logged in as {username}!\n")
    return username

def banking_menu(username):
    while True:
        print("--- Banking Menu ---")
        print("1) View balance")
        print("2) Deposit")
        print("3) Withdraw")
        print("4) Logout")
        choice = input("Choose: ").strip()

        if choice == "1":
            print(f"Balance: ${accounts[username]['balance']:.2f}\n")

        elif choice == "2":
            amount = input("Deposit amount: ").strip()
            if not amount.replace(".", "", 1).isdigit():
                print("Please enter a valid number.\n")
                continue
            amount = float(amount)
            if amount <= 0:
                print("Amount must be greater than 0.\n")
                continue
            accounts[username]["balance"] += amount
            print("Deposit successful!\n")

        elif choice == "3":
            amount = input("Withdraw amount: ").strip()
            if not amount.replace(".", "", 1).isdigit():
                print("Please enter a valid number.\n")
                continue
            amount = float(amount)
            if amount <= 0:
                print("Amount must be greater than 0.\n")
                continue
            if amount > accounts[username]["balance"]:
                print("Not enough money.\n")
                continue
            accounts[username]["balance"] -= amount
            print("Withdrawal successful!\n")

        elif choice == "4":
            print("Logged out.\n")
            break

        else:
            print("Pick 1-4.\n")

def main():
    while True:
        print("--- Mini Banking System ---")
        print("1) Create account")
        print("2) Login")
        print("3) Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            user = login()
            if user:
                banking_menu(user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Pick 1-3.\n")

main()