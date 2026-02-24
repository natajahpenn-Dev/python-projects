contacts = {}

while True:
    print("\n--- Contact Book ---")
    print("1. Add contact")
    print("2. Show contacts")
    print("3. Delete contact")
    print("4. Quit")

    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter name: ")
        phone = input("Enter phone number: ")
        contacts[name] = phone
        print("Contact added!")

    elif choice == "2":
        if not contacts:
            print("No contacts found.")
        else:
            for name, phone in contacts.items():
                print(f"{name}: {phone}")

    elif choice == "3":
        name = input("Enter name to delete: ")
        if name in contacts:
            del contacts[name]
            print("Contact deleted!")
        else:
            print("Contact not found.")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")