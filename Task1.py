class ContactMaster:
    def __init__(self):
        self.contacts = []

    def add_contact(self):
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        if name and phone:
            self.contacts.append((name, phone))
            print(f"Contact '{name}' added successfully.")
        else:
            print("Both name and phone number are required.")

    def delete_contact(self):
        self.view_contacts()
        try:
            index = int(input("Enter the number of the contact to delete: ")) - 1
            if 0 <= index < len(self.contacts):
                removed = self.contacts.pop(index)
                print(f"Deleted contact: {removed[0]} - {removed[1]}")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

    def search_contacts(self):
        query = input("Enter name or phone to search: ").lower()
        results = [c for c in self.contacts if query in c[0].lower() or query in c[1]]
        if results:
            print("Search Results:")
            for i, (name, phone) in enumerate(results, 1):
                print(f"{i}. {name} - {phone}")
        else:
            print("No contacts found.")

    def view_contacts(self):
        if self.contacts:
            print("\nContact List:")
            for i, (name, phone) in enumerate(self.contacts, 1):
                print(f"{i}. {name} - {phone}")
        else:
            print("No contacts to display.")

    def run(self):
        while True:
            print("\n--- ContactMaster Menu ---")
            print("1. Add Contact")
            print("2. Delete Contact")
            print("3. Search Contact")
            print("4. View All Contacts")
            print("5. Exit")
            choice = input("Enter your choice (1-5): ")
            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.delete_contact()
            elif choice == '3':
                self.search_contacts()
            elif choice == '4':
                self.view_contacts()
            elif choice == '5':
                print("Exiting ContactMaster. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = ContactMaster()
    app.run()