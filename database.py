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


# 🔥 FIXED INSERT (NORMALIZED STORAGE)
def insert(text, score, sentiment):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    text_clean = text.strip().lower()   # ✅ important fix

    cursor.execute(
        "INSERT INTO reviews(text, score, sentiment, created_at) VALUES (?, ?, ?, ?)",
        (text_clean, score, sentiment, timestamp)
    )
    conn.commit()


# 🔥 FIXED EXISTS (NORMALIZED CHECK)
def exists(text):
    text_clean = text.strip().lower()

    cursor.execute("SELECT 1 FROM reviews WHERE text = ?", (text_clean,))
    return cursor.fetchone() is not None


def fetch_all():
    cursor.execute("SELECT * FROM reviews ORDER BY id DESC")
    return cursor.fetchall()


def clear_data():
    cursor.execute("DELETE FROM reviews")
    conn.commit()
