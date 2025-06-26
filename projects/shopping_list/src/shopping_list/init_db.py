#!/usr/bin/env python3

import os
import sqlite3

# Get the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Create the full path to the database file
db_path = os.path.join(basedir, "database.db")

connection = sqlite3.connect(db_path)

# Get the full path to schema.sql
schema_path = os.path.join(basedir, "schema.sql")

with open(schema_path) as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO posts (title, content) VALUES (?, ?)",
    ("First Post", "Content for the first post"),
)

cur.execute(
    "INSERT INTO posts (title, content) VALUES (?, ?)",
    ("Second Post", "Content for the second post"),
)

connection.commit()
connection.close()
