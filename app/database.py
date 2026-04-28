import sqlite3
import hashlib
from pathlib import Path

DB_PATH = Path("mentor_clean_code.db")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_user(username: str, password: str) -> bool:
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )

        connection.commit()
        connection.close()
        return True

    except sqlite3.IntegrityError:
        return False


def verify_user(username: str, password: str) -> bool:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return False

    stored_password_hash = row[0]
    return stored_password_hash == hash_password(password)


def create_default_admin():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    admin_exists = cursor.fetchone()

    connection.close()

    if not admin_exists:
        create_user("admin", "1234")