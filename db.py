import sqlite3

def get_db():
    conn = sqlite3.connect("leave.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    create_tables(conn)
    return conn


def create_tables(conn):
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT,
        is_active INTEGER DEFAULT 1
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS leave_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        total INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        leave_type_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        days INTEGER,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(leave_type_id) REFERENCES leave_types(id)
    )
    """)

    conn.commit()
