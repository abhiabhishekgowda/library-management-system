import sqlite3

def create_database():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    create_table = """
        CREATE TABLE IF NOT EXISTS BOOKS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            available INTEGER
        )
    """
    cursor.execute(create_table)
    conn.commit()
    conn.close()

def add_book():
    title = input("Enter title name: ").strip().lower()
    author = input("Enter author name: ").strip().lower()

    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        query = "INSERT INTO BOOKS(title, author, available) VALUES(?, ?, ?)"
        cursor.execute(query, (title, author, 1))
        conn.commit()
        print(f"Title: '{title}' by {author} added successfully.")

def view_all_books():
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BOOKS")
        result = cursor.fetchall()

        print("\n---- LIST OF BOOKS ----")
        if not result:
            print("Sorry, the library is currently empty.")
        else:
            for row in result:
                status = "Available" if row[3] == 1 else "Borrowed"
                print(f"ID: {row[0]} | TITLE: {row[1]} | AUTHOR: {row[2]} | STATUS: {status}")

def search_books():
    keyword = input("Enter title or author to search: ").strip().lower()
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM BOOKS WHERE title LIKE ? OR author LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
        result = cursor.fetchall()

        print("\n---- SEARCH RESULTS ----")
        if not result:
            print(f"No book found with that name: {keyword}")
        else:
            for row in result:
                status = "Available" if row[3] == 1 else "Borrowed"
                print(f"ID: {row[0]} | TITLE: {row[1]} | AUTHOR: {row[2]} | STATUS: {status}")

def borrow_book():
    try:
        book_id = int(input("\nEnter the ID of the book you want to borrow: "))
    except ValueError:
        print("Invalid input. Please enter a valid book ID (number).")
        return

    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT available FROM BOOKS WHERE id = ?", (book_id,))
        row = cursor.fetchone()

        if row is None:
            print(f"No book found with ID: {book_id}")
        elif row[0] == 0:
            print(f"Book with ID {book_id} is already borrowed.")
        else:
            cursor.execute("UPDATE BOOKS SET available = 0 WHERE id = ?", (book_id,))
            conn.commit()
            print(f"Book with ID {book_id} has been borrowed successfully.")

def main():
    create_database()
    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Books")
        print("4. Borrow Book")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_all_books()
        elif choice == "3":
            search_books()
        elif choice == "4":
            borrow_book()
        elif choice == "5":
            print("Exiting the library system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()