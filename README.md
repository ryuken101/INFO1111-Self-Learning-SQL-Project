# INFO1111-Self-Learning-SQL-Project

Personal Book Tracker
A small Python + SQLite mini-project for a SQL coursework task. It records
the books I have read, the authors who wrote them, and a 1–5 rating for
each book. The script demonstrates a set of core SQL features through
parameterised queries from Python's built-in sqlite3 module, so the
application is safe from SQL injection.
How to run
Requirements: Python 3.7+. No third-party packages are needed.
bashgit clone <repo-url>
cd book-tracker
python book_tracker.py
A single run of the script will:

Create a fresh books.db SQLite database from schema.sql.
Seed it with 3 authors and 6 books.
Run one demo per required SQL feature and print the result.
Attempt four invalid inserts to show that each schema constraint is
enforced (the script catches the IntegrityError from SQLite and prints
the rejection reason).

You can re-run the script as many times as you like — the database is
rebuilt from scratch every time, so the state never drifts.
Schema
Defined in schema.sql. Two tables, connected by a foreign key.
authors
ColumnTypeConstraintsauthor_idINTEGERPRIMARY KEYnameTEXTNOT NULL, UNIQUEnationalityTEXT(nullable)
books
ColumnTypeConstraintsbook_idINTEGERPRIMARY KEYtitleTEXTNOT NULLauthor_idINTEGERNOT NULL, FOREIGN KEY → authors(author_id)year_publishedINTEGER(nullable)ratingINTEGERNOT NULL, CHECK (rating BETWEEN 1 AND 5)
SQLite turns foreign-key enforcement off by default, so the Python code
runs PRAGMA foreign_keys = ON; every time it opens a connection (see
get_connection() in book_tracker.py).
Queries
Each query in book_tracker.py lives inside its own function and has a
header comment naming the SQL feature it demonstrates.
FunctionSQL feature demonstratedWhat it doesseed_dataINSERT (parameterised)Adds the initial authors and books.demo_updateUPDATE with WHERERaises the rating of Animal Farm to 5.demo_deleteDELETE with WHERERemoves one book by title.demo_select_whereSELECT … WHERELists every book that has a 5-star rating.demo_inner_joinINNER JOINPairs each book with its author's name and nationality.demo_order_byORDER BYLists every book sorted by rating descending, then title alphabetically.demo_group_by_aggregateGROUP BY with COUNT and AVGFor each author, computes the count of books and the average rating.demo_constraint_enforcementConstraint enforcementAttempts four invalid inserts; each raises sqlite3.IntegrityError.
All queries use ? placeholders with values supplied as a tuple, so
user-supplied values are passed as parameters rather than concatenated
into SQL strings. This is what protects against SQL injection.
Constraint enforcement
demo_constraint_enforcement tries four invalid inserts and prints the
rejection reason from SQLite for each:

NOT NULL on books.title — insert with title = NULL.
UNIQUE on authors.name — insert a second "George Orwell".
FOREIGN KEY on books.author_id — insert a book with
author_id = 999 (no such author).
CHECK on books.rating — insert a book with rating = 10.

Each attempt is wrapped in try / except sqlite3.IntegrityError so the
script keeps going and reports which constraint blocked the row.
Example output
Constraint enforcement checks:
  [OK] NOT NULL on books.title rejected: NOT NULL constraint failed: books.title
  [OK] UNIQUE on authors.name rejected: UNIQUE constraint failed: authors.name
  [OK] FOREIGN KEY on books.author_id rejected: FOREIGN KEY constraint failed
  [OK] CHECK on books.rating rejected: CHECK constraint failed: rating BETWEEN 1 AND 5
Files

book_tracker.py — main script (initialises DB, seeds data, runs all demos).
schema.sql — schema definition (tables, constraints, foreign key).
README.md — this file.
.gitignore — keeps the generated books.db and Python caches out of the repo.