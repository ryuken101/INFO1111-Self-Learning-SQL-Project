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

def demo_select_where():
    """List every book that has the maximum rating."""
    conn = get_connection()
    cur = conn.cursor()
 
    # ---- SQL FEATURE: SELECT ... WHERE -------------------------------------
    # Find every book with a rating equal to 5.
    cur.execute(
        "SELECT title, rating FROM books WHERE rating = ?;",
        (5,),
    )
    rows = cur.fetchall()
 
    conn.close()
    print("SELECT ... WHERE rating = 5:")
    for title, rating in rows:
        print(f"  {rating} stars - {title}")
    print()

def demo_inner_join():
    """Pair each book with the author who wrote it."""
    conn = get_connection()
    cur = conn.cursor()
 
    # ---- SQL FEATURE: INNER JOIN -------------------------------------------
    # Join books with authors so each row includes the author's name and
    # nationality alongside the book title.
    cur.execute("""
        SELECT books.title, authors.name, authors.nationality
        FROM   books
        INNER JOIN authors ON books.author_id = authors.author_id;
    """)
    rows = cur.fetchall()
 
    conn.close()
    print("INNER JOIN books x authors:")
    for title, name, nationality in rows:
        print(f"  '{title}' by {name} ({nationality})")
    print()

def demo_order_by():
    """List every book sorted by rating, then title."""
    conn = get_connection()
    cur = conn.cursor()
 
    # ---- SQL FEATURE: ORDER BY ---------------------------------------------
    # Sort books by rating (highest first), tie-breaking alphabetically.
    cur.execute("""
        SELECT title, rating
        FROM   books
        ORDER BY rating DESC, title ASC;
    """)
    rows = cur.fetchall()
 
    conn.close()
    print("ORDER BY rating DESC, title ASC:")
    for title, rating in rows:
        print(f"  {rating} stars - {title}")
    print()

def demo_group_by_aggregate():
    """For each author, show how many books they have and their average rating."""
    conn = get_connection()
    cur = conn.cursor()
 
    # ---- SQL FEATURE: GROUP BY with aggregates (COUNT, AVG) ----------------
    # Group books by author and compute the count and average rating per author.
    cur.execute("""
        SELECT authors.name,
               COUNT(books.book_id)  AS book_count,
               AVG(books.rating)     AS avg_rating
        FROM   authors
        INNER JOIN books ON authors.author_id = books.author_id
        GROUP BY authors.author_id, authors.name
        ORDER BY avg_rating DESC;
    """)
    rows = cur.fetchall()
 
    conn.close()
    print("GROUP BY author (book count, average rating):")
    for name, count, avg in rows:
        print(f"  {name}: {count} book(s), avg {avg:.2f} stars")
    print()