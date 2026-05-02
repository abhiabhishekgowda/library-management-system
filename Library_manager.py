import sqlite3
from datetime import datetime

DB_NAME = "library.db"

def create_database():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        create_table = """
            CREATE TABLE IF NOT EXISTS BOOKS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            available INTEGER DEFAULT 1)
        """
        cursor.execute(create_table)
        conn.commit()

def migrate_schema():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Add timestamp column
        try:
            cursor.execute("ALTER TABLE BOOKS ADD COLUMN timestamp TEXT")
        except sqlite3.OperationalError:
            pass
        # Add borrowed_date column
        try:
            cursor.execute("ALTER TABLE BOOKS ADD COLUMN borrowed_date TEXT")
        except sqlite3.OperationalError:
            pass
        # Add returned_date column
        try:
            cursor.execute("ALTER TABLE BOOKS ADD COLUMN returned_date TEXT")
        except sqlite3.OperationalError:
            pass
        conn.commit()

def get_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_book():
    title = input("Enter Title Name: ").strip()
    author = input("Enter Author Name: ").strip()

    if not title or not author:
        print("Title and Author cannot be empty.")
        return

    now = get_datetime()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        query = "INSERT INTO BOOKS (title, author, available, timestamp) VALUES (?,?,?,?)"
        cursor.execute(query, (title, author, 1, now))
        conn.commit()
        print(f"Title: {title} | Author: {author} | Added: {now} successfully.")

def view_all_books():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BOOKS")
        rows = cursor.fetchall()

        print("\n----- LIST OF BOOKS -----")
        if not rows:
            print("The library is empty.")
        else:
            for row in rows:
                status = "Available" if row[3] == 1 else "Borrowed"
                added = row[4] if row[4] else "Not recorded"
                borrowed = row[5] if row[5] else "Never borrowed"
                returned = row[6] if row[6] else "Never returned"

                print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Status: {status}")
                print(f"   Added: {added} | Borrowed: {borrowed} | Returned: {returned}")

def search_book():
    keyword = input("Enter Title or Author to search: ").strip()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM BOOKS WHERE title LIKE ? OR author LIKE ?"
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()

        print("\n----- SEARCH RESULTS -----")
        if not rows:
            print(f"No book found with that name: {keyword}")
        else:
            for row in rows:
                status = "Available" if row[3] == 1 else "Borrowed"
                added = row[4] if row[4] else "Not recorded"
                borrowed = row[5] if row[5] else "Never borrowed"
                returned = row[6] if row[6] else "Never returned"

                print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Status: {status}")
                print(f"   Added: {added} | Borrowed: {borrowed} | Returned: {returned}")

def borrow_book():
    try:
        book_id = int(input("Enter the Book ID you want to borrow: "))
    except ValueError:
        print("Invalid input. Please enter a valid ID (number).")
        return

    now = get_datetime()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT available FROM BOOKS WHERE id = ?", (book_id,))
        row = cursor.fetchone()

        if row is None:
            print(f"No book found with ID: {book_id}")
        elif row[0] == 0:
            print(f"Book ID {book_id} is already borrowed.")
        else:
            cursor.execute("UPDATE BOOKS SET available = 0, borrowed_date = ? WHERE id = ?", (now, book_id))
            conn.commit()
            print(f"Book ID {book_id} has been successfully borrowed at {now}.")

def return_book():
    try:
        book_id = int(input("Enter the Book ID you want to return: "))
    except ValueError:
        print("Invalid input. Please enter a valid ID (number).")
        return

    now = get_datetime()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT available FROM BOOKS WHERE id = ?", (book_id,))
        row = cursor.fetchone()

        if row is None:
            print(f"No book found with ID: {book_id}")
        elif row[0] == 1:
            print(f"Book ID {book_id} is already available. No need to return.")
        else:
            cursor.execute("UPDATE BOOKS SET available = 1, returned_date = ? WHERE id = ?", (now, book_id))
            conn.commit()
            print(f"Book ID {book_id} has been successfully returned at {now}.")

def delete_book():
    try:
        book_id = int(input("Enter the Book ID you want to delete: "))
    except ValueError:
        print("Invalid input. Please enter a valid ID (number).")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BOOKS WHERE id = ?", (book_id,))
        row = cursor.fetchone()

        if row is None:
            print(f"No book found with ID: {book_id}")
        else:
            user_confirmation = input(f"Are you sure you want to delete book ID {book_id}? (yes/no): ").strip().lower()
            if user_confirmation in ["yes", "y"]:
                cursor.execute("DELETE FROM BOOKS WHERE id = ?", (book_id,))
                conn.commit()
                print(f"Book ID {book_id} has been successfully deleted.")
            else:
                print("Deletion cancelled. The book was not deleted.")

def main():
    create_database()
    migrate_schema()
    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Delete Book")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            view_all_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            borrow_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            delete_book()
        elif choice == "7":
            print("Exiting the library system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()