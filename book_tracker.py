import os 
import sqlite3

DB_PATH = "books.db"
SCHEMA_PATH = "schema.sql"


# Setup Functions 

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
 