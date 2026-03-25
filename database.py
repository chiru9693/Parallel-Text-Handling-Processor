import sqlite3
from datetime import datetime

conn = sqlite3.connect("reviews.db", check_same_thread=False)
cursor = conn.cursor()

def create_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        score INTEGER,
        sentiment TEXT,
        created_at TEXT
    )
    """)
    conn.commit()

def insert(text, score, sentiment):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO reviews(text, score, sentiment, created_at) VALUES (?, ?, ?, ?)",
        (text, score, sentiment, timestamp)
    )
    conn.commit()

def fetch_all():
    cursor.execute("SELECT * FROM reviews ORDER BY id DESC")
    return cursor.fetchall()

def clear_data():
    cursor.execute("DELETE FROM reviews")
    conn.commit()