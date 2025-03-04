import datetime
import os

class LMS:
    """
    Library Management System with:
    1. Display Books
    2. Issue Books
    3. Add Books
    4. Return Books
    """

    def __init__(self, list_of_books, library_name):
        self.list_of_books = list_of_books
        self.library_name = library_name
        self.books_dict = {}
        self.load_books()

    def load_books(self):
        """Loads books from the text file into a dictionary."""
        if not os.path.exists(self.list_of_books):
            print("Error: Book list file not found!")
            return

        with open(self.list_of_books, "r") as file:
            books = file.readlines()

        for id, title in enumerate(books, start=101):
            self.books_dict[str(id)] = {
                "title": title.strip(),
                "lender": "",
                "lend_date": "",
                "status": "Available"
            }

    def display_books(self):
        """Displays all books in the library."""
        print("\n------ Available Books ------")
        print("ID\tTitle\t\tStatus")
        print("-----------------------------")
        for book_id, book in self.books_dict.items():
            print(f"{book_id}\t{book['title'][:20]} - [{book['status']}]")

    def issue_book(self):
        """Allows a user to issue a book."""
        self.display_books()
        book_id = input("\nEnter Book ID to Issue: ")

        if book_id in self.books_dict:
            if self.books_dict[book_id]["status"] == "Available":
                user_name = input("Enter Your Name: ")
                self.books_dict[book_id]["lender"] = user_name
                self.books_dict[book_id]["lend_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.books_dict[book_id]["status"] = "Issued"
                print("Book issued successfully!")
            else:
                print(f"Book is already issued to {self.books_dict[book_id]['lender']} on {self.books_dict[book_id]['lend_date']}.")
        else:
            print("Invalid Book ID!")

    def add_book(self):
        """Adds a new book to the library and updates the file."""
        new_book = input("\nEnter Book Title: ").strip()
        if not new_book:
            print("Book title cannot be empty!")
            return

        with open(self.list_of_books, "a") as file:
            file.write(new_book + "\n")

        new_id = str(max(map(int, self.books_dict.keys()), default=100) + 1)
        self.books_dict[new_id] = {"title": new_book, "lender": "", "lend_date": "", "status": "Available"}
        print(f"Book '{new_book}' added successfully!")

    def return_book(self):
        """Handles book return process."""
        book_id = input("\nEnter Book ID to Return: ")

        if book_id in self.books_dict:
            if self.books_dict[book_id]["status"] == "Issued":
                self.books_dict[book_id]["lender"] = ""
                self.books_dict[book_id]["lend_date"] = ""
                self.books_dict[book_id]["status"] = "Available"
                print("Book returned successfully!")
            else:
                print("Book is already in the library!")
        else:
            print("Invalid Book ID!")

if __name__ == "__main__":
    library = LMS("list_of_books.txt", "My Library")

    actions = {
        "D": ("Display Books", library.display_books),
        "I": ("Issue Book", library.issue_book),
        "A": ("Add Book", library.add_book),
        "R": ("Return Book", library.return_book),
        "Q": ("Quit", None)
    }

    while True:
        print("\n--- Library Menu ---")
        for key, (desc, _) in actions.items():
            print(f"Press {key} to {desc}")

        choice = input("Choose an option: ").upper()
        if choice == "Q":
            print("Exiting Library System...")
            break
        elif choice in actions:
            actions[choice][1]()  # Call the corresponding function
        else:
            print("Invalid choice! Try again.")
