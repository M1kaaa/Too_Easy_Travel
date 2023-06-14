import sqlite3 as sq

with sq.connect("database.db") as con:
    cur = con.cursor() #Cursor

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    req_count INTEGER,
    city TEXT
    )""")

