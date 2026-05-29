
-- Personal Book Tracker - database schema
-- Two tables (authors and books) connected by a foreign key.
--
-- Constraints used:
--   * PRIMARY KEY  on author_id and book_id
--   * NOT NULL     on every required field
--   * UNIQUE       on authors.name (no two authors with the same name)
--   * FOREIGN KEY  books.author_id -> authors.author_id
--   * CHECK        books.rating is between 1 and 5 inclusive
--
-- Note: SQLite requires foreign-key enforcement to be enabled per-connection
-- using `PRAGMA foreign_keys = ON;`. The Python code does this in
-- get_connection() so the constraint is actually enforced at runtime.
 
CREATE TABLE authors (
    author_id   INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL UNIQUE,
    nationality TEXT
);
 
CREATE TABLE books (
    book_id        INTEGER PRIMARY KEY,
    title          TEXT    NOT NULL,
    author_id      INTEGER NOT NULL,
    year_published INTEGER,
    rating         INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);
 