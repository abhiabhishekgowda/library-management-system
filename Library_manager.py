import sqlite3

def create_table():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BOOKS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            available INTEGER
        )
        """)
    conn.commit()

def add_book(title,author):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO BOOKS (title,author,available) VALUES (?,?,?)",
            (title,author,1)
        )
        conn.commit()
        print(f" Book '{title}' by {author} added successfully!") 

def view_all_books():
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, available FROM BOOKS")
        rows = cursor.fetchall()

        print("\n--- YOUR PERMANENT LIBRARY ---")
        if not rows:
            print("NO books the library emty")
        else:
            for row in rows:
                print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]}")

def main():
    create_table()
    title = input("Enter title name: ")
    author = input("Enter author name: ")
    add_book(title, author)
    view_all_books()
    print("🎉 Day one done!")

if __name__ == "__main__":
    main()