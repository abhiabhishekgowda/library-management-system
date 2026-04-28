import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect("librarys.db")
    cursor = conn.cursor()
    create_table = """
        CREATE TABLE IF NOT EXISTS BOOKS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            available INTEGER)
    """
    cursor.execute(create_table)
    conn.commit()
    conn.close()

def add_books():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    title = input("Enter Title Name: ")
    author = input("Enter Author Name: ")

    with sqlite3.connect("librarys.db") as conn:
        cursor = conn.cursor()
        query = "INSERT INTO BOOKS (title,author,available) VALUES (?,?,?)"
        cursor.execute(query,(title,author,1,))
        conn.commit()
        print(f"Title: {title} By: {author} Added Succeefully.")

def view_all_books():
    with sqlite3.connect("librarys.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BOOKS")
        rows = cursor.fetchall()

        print("\n-----THE LITS OF BOOKS ARE------")
        if not rows:
            print("The Library is empty.")
        else:
            for row in rows:
                status = "Available" if row[3] == 1 else "Borrowed"
                print(f"ID: {row[0]} | TITLE: {row[1]} | AUTHOR: {row[2]} | {status}")

def search_books():
    keyword = input("Enter Title or Author to search: ")
    with sqlite3.connect("librarys.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BOOKS WHERE title LIKE ? or author LIKE ?",
            (f"%{keyword}%",f"%{keyword}%"))
        rows = cursor.fetchall()

        print("\n----THE SEARCH RESULTS ARE-----")
        if not rows:
            print(f"No Books Found With That Name: {keyword}.")
        else:
            for row in rows:
                status = "Available" if row[3] == 1 else "Borrowed"
                print(f"ID: {row[0]} | TITLE: {row[1]} | AUTHOR: {row[2]} | {status}")

def borrow_books():
    try:
        book_id = int(input("Enter The ID of Books That You Want To Borrow: "))
    except ValueError:
        print("Invaild Input. Plase enter vaild book ID (number)")
        return

    with sqlite3.connect("librarys.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BOOKS WHERE id = ?",(book_id,))
        rows = cursor.fetchone()

        if rows is None:
            print(f"No Books Found With That ID: {book_id}.")
        elif rows[3] == 0:
            print(f"The ID: {book_id} Book is alredy borrowed.")
        else:
            cursor.execute("UPDATE BOOKS SET available = 0 WHERE id = ?",(book_id,))
            conn.commit()
            print(f"The ID: {book_id} Book Succeefully borrowed.")

def return_books():
    try:
        book_id = int(input("Enter The ID of Books That You Want To Return: "))
    except ValueError:
        print("Invaild Input. Plase enter vaild book ID (number)")
        return

    with sqlite3.connect("librarys.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BOOKS WHERE id = ?",(book_id,))
        rows = cursor.fetchone()

        if rows is None:
            print(f"No Books Found With That ID: {book_id}.")
        elif rows[3] == 1:
            print(f"The ID: {book_id} Book is alredy available no need to return.")
        else:
            cursor.execute("UPDATE BOOKS SET available = 1 WHERE id = ?",(book_id,))
            conn.commit()
            print(f"The ID: {book_id} Book Succeefully Return.")

def delete_book():
    try:
        book_id = int(input("Enter The ID of Books That You Want To Delect: "))
    except ValueError:
        print("Invaild Input. Plase enter vaild book ID (number)")
        return

    with sqlite3.connect("librarys.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BOOKS WHERE id = ?",(book_id,))
        row = cursor.fetchone()

        if row is None:
            print(f"No Books Found With That ID: {book_id}.")
        else:
            user_confirmation = input(f"Are you sure you want to delete the book with ID {book_id}? (yes/no): ").strip().lower()
            if user_confirmation == "yes":
                cursor.execute("DELETE FROM BOOKS WHERE id = ?",(book_id,))
                conn.commit()
                print(f"Book with ID {book_id} has been deleted successfully.")
            else:                
                print("Deletion cancelled. The book was not deleted.")

def main():
    create_database()
    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Books")
        print("4. Borrow Book")
        print("5. Return Books")
        print("6. Delete Books")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            add_books()
        elif choice == "2":
            view_all_books()
        elif choice == "3":
            search_books()
        elif choice == "4":
            borrow_books()
        elif choice == "5":
            return_books()
        elif choice == "6":
            delete_book()
        elif choice == "7":
            print("Exiting the library system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
            