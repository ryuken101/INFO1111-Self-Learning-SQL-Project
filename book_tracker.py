import os 
import sqlite3

DB_PATH = "books.db"
SCHEMA_PATH = "schema.sql"


# -------- Setup Functions --------

def get_connection():
    """Open a SQLite connection with foreign-key enforcement turned ON."""
    conn = sqlite3.connect(DB_PATH)
    # Foreign keys are off by default in SQLite; turn them on every connection.
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
 
 
def initialise_database():
    """(Re)create the database from schema.sql so each run starts fresh."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# -------- SQL feature demonstrations --------
# -------- Each function exercises one of the required SQL features. --------

def seed_data():
    """Populate authors and books with example rows."""
    conn = get_connection()
    cur = conn.cursor()
 
    # ---- SQL FEATURE: INSERT (parameterised) -------------------------------
    # Insert several authors. Using ? placeholders + a tuple of values means
    # user input is passed as a parameter, not concatenated into the SQL.
    authors = [
        ("George Orwell",     "British"),
        ("Ursula K. Le Guin", "American"),
        ("Italo Calvino",     "Italian"),
    ]
    cur.executemany(
        "INSERT INTO authors (name, nationality) VALUES (?, ?);",
        authors,
    )
 
    # ---- SQL FEATURE: INSERT (parameterised) -------------------------------
    # Insert books, referencing authors by their foreign-key id.
    books = [
        ("1984",                              1, 1949, 5),
        ("Animal Farm",                       1, 1945, 4),
        ("The Dispossessed",                  2, 1974, 5),
        ("A Wizard of Earthsea",              2, 1968, 4),
        ("Invisible Cities",                  3, 1972, 5),
        ("If on a winter's night a traveler", 3, 1979, 3),
    ]
    cur.executemany(
        "INSERT INTO books (title, author_id, year_published, rating) "
        "VALUES (?, ?, ?, ?);",
        books,
    )
 
    conn.commit()
    conn.close()
    print("Seeded 3 authors and 6 books.\n")

def demo_update():
    """Bump the rating of one book."""
    conn = get_connection()
    cur = conn.cursor()
 
    # ---- SQL FEATURE: UPDATE (with WHERE) ----------------------------------
    # Change the rating of 'Animal Farm' from 4 to 5.
    cur.execute(
        "UPDATE books SET rating = ? WHERE title = ?;",
        (5, "Animal Farm"),
    )
 
    conn.commit()
    conn.close()
    print("UPDATE: changed the rating of 'Animal Farm' to 5.")

def demo_delete():
    """Remove a book by title."""
    conn = get_connection()
    cur = conn.cursor()
 
    # ---- SQL FEATURE: DELETE (with WHERE) ----------------------------------
    # Remove the book "If on a winter's night a traveler" from the library.
    cur.execute(
        "DELETE FROM books WHERE title = ?;",
        ("If on a winter's night a traveler",),
    )
 
    conn.commit()
    conn.close()
    print("DELETE: removed 'If on a winter's night a traveler'.\n")