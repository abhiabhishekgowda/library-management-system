
import sqlite3

def initialize_library():
    # 1. Connect to the database file
    conn = sqlite3.connect("library.db")

    # 2. Create a 'cursor'
    cursor = conn.cursor()

    # 3. Create the table if it doesn't exist
    create_table = """
    CREATE TABLE IF NOT EXISTS BOOKS(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        available INTEGER
    )
    """
    cursor.execute(create_table)

    title = input("Enter title name: ")
    author = input("Enter author name: ")

    query = """
    INSERT INTO BOOKS(title, author, available)
    VALUES (?, ?, ?)"""

    cursor.execute(query,(title,author,1))
    # 4. Commit and close
    conn.commit()
    conn.close()
    print("Book added successfully")

if __name__ == "__main__":
    initialize_library()
