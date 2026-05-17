import sqlite3
from datetime import datetime

DB_NAME = "library.db"

def create_database():
    """Create the books table if it does not exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            available INTEGER DEFAULT 1
        )
        """)
        conn.commit()

def migrate_schema():
    """Add extra columns if they do not exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        for column in ["timestamp TEXT", "borrowed_date TEXT", "returned_date TEXT","borrowed_by TEXT"]:
            try:
                cursor.execute(f"ALTER TABLE books ADD COLUMN {column}")
            except sqlite3.OperationalError:
                pass
        conn.commit()

def get_date_time():
    """Return current date and time as string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_book():
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()

    if not title or not author:
        print("Title and Author cannot be empty.")
        return

    now = get_date_time()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, available, timestamp) VALUES (?, ?, ?, ?)",
                       (title, author, 1, now))
        conn.commit()
        print(f"Book '{title}' by {author} added successfully at {now}.")

def view_all_books():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()

        print("\n--- All Books ---")
        if not rows:
            print("Library is currently empty.")
        else:
            for row in rows:
                status = "Available" if row[3] == 1 else "Borrowed"
                added = row[4] or "Not recorded"
                borrowed = row[5] or "Never borrowed"
                returned = row[6] or "Never returned"
                borrowed_by = row[7] or "N/A"

                print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Status: {status}")
                print(f"   Added: {added} | Borrowed: {borrowed} | Returned: {returned}")
                print(f"   Borrowed by: {borrowed_by}")

def view_borrowed_books():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE available = 0")
        rows = cursor.fetchall()

        print("\n--- Borrowed Books ---")
        if not rows:
            print("No books are currently borrowed.")
        else:
            for row in rows:
                borrowed = row[5] or "Never borrowed"
                borrowed_by = row[7] or "Unknown"
                print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Borrowed at: {borrowed} | Borrowed by: {borrowed_by}")

def search_books():
    keyword = input("Enter title or author to search: ").strip()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                       (f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()

        print("\n--- Search Results ---")
        if not rows:
            print(f"No books found matching: {keyword}")
        else:
            for row in rows:
                status = "Available" if row[3] == 1 else "Borrowed"
                print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Status: {status}")

def borrow_book():
    try:
        book_id = int(input("Enter the Book ID to borrow: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    user_name = input("Enter Your Name: ").strip()
    now = get_date_time()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT available, title, author FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()

        if row is None:
            print(f"No book found with ID {book_id}.")
        elif row[0] == 0:
            print(f"Book '{row[1]}' is already borrowed.")
        else:
            cursor.execute("UPDATE books SET available = 0 ,borrowed_date = ?, borrowed_by = ? WHERE id = ?", (now, user_name, book_id))
            conn.commit()
            print(f"{user_name} borrowed '{row[1]}' by {row[2]} at {now}.")

def return_book():
    try:
        book_id = int(input("Enter the Book ID to return: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    now = get_date_time()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT available, title, author, borrowed_by FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()

        if row is None:
            print(f"No book found with ID {book_id}.")
        elif row[0] == 1:
            print(f"Book '{row[1]}' is already available.")
        else:
            cursor.execute("UPDATE books SET available = 1, returned_date = ?, borrowed_by = NULL WHERE id = ?", (now, book_id))
            conn.commit()
            print(f"{row[3]} returned '{row[1]}' by {row[2]} at {now}.")

def delete_book():
    try:
        book_id = int(input("Enter the Book ID to delete: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()

        if row is None:
            print(f"No book found with ID {book_id}.")
        elif row[3] == 0:
            print(f"Book '{row[1]}' is borrowed. Cannot delete borrowed books.")
        else:
            confirm = input(f"Are you sure you want to delete '{row[1]}'? (yes/no): ").strip().lower()
            if confirm in ["yes", "y"]:
                cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
                conn.commit()
                print(f"Book '{row[1]}' deleted successfully.")
            else:
                print("Deletion cancelled.")

def view_books_by_user():
    user_name = input("Enter user name: ").strip()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE borrowed_by = ?", (user_name,))
        rows = cursor.fetchall()

        print(f"\n--- Books borrowed by {user_name} ---")
        if not rows:
            print(f"{user_name} has not borrowed any books.")
        else:
            for row in rows:
                borrowed = row[5] or "Never borrowed"
                print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Borrowed at: {borrowed}")


def main():
    create_database()
    migrate_schema()
    while True:
        print("\n--- Library Menu ---")
        print("1. Add a Book")
        print("2. View All Books")
        print("3. View Borrowed Books")
        print("4. Search Books")
        print("5. Borrow a Book")
        print("6. Return a Book")
        print("7. Delete a Book")
        print("8. View Books by User")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ").strip()
        if choice == "1":
            add_book()
        elif choice == "2":
            view_all_books()
        elif choice == "3":
            view_borrowed_books()
        elif choice == "4":
            search_books()
        elif choice == "5":
            borrow_book()
        elif choice == "6":
            return_book()
        elif choice == "7":
            delete_book()
        elif choice == "8":
            view_books_by_user()
        elif choice == "9":
            print("Exiting the library system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()

