# INFO1111-Self-Learning-SQL-Project

Personal Book Tracker

A small Python + SQLite mini-project for a SQL coursework task. It records
the books I have read, the authors who wrote them, and a 1–5 rating for
each book. The script demonstrates a set of core SQL features through
parameterised queries from Python's built-in sqlite3 module, so the
application is safe from SQL injection.

How to run


A single run of the script will:

1. Create a fresh books.db SQLite database from schema.sql.
2. Seed it with 3 authors and 6 books.
3. Run one demo per required SQL feature and print the result.
4. Attempt four invalid inserts to show that each schema constraint is
enforced (the script catches the IntegrityError from SQLite and prints
the rejection reason).

You can re-run the script as many times as you like — the database is
rebuilt from scratch every time, so the state never drifts.
