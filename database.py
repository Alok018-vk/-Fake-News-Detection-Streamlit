import sqlite3

DB_NAME = "news_history.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news TEXT,
            prediction TEXT,
            score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_prediction(news, prediction, score):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        "INSERT INTO predictions (news, prediction, score) VALUES (?, ?, ?)",
        (news, prediction, score)
    )

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_NAME)

    records = conn.execute(
        "SELECT * FROM predictions ORDER BY id DESC"
    ).fetchall()

    conn.close()
    return records
