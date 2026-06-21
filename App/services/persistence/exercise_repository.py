import sqlite3
import streamlit as st
from pathlib import Path
import hashlib

_DB_PATH = "/tmp/data.db"

def _hash(password: str) -> str:
    return hashlib.sha256(password.strip().encode()).hexdigest()


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = _get_connection()

    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL REFERENCES users(id),
                exercise_name TEXT    NOT NULL,
                reps          INTEGER NOT NULL DEFAULT 0,
                sets          INTEGER NOT NULL DEFAULT 0,
                time          INTEGER NOT NULL DEFAULT 0,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def get_user(username: str) -> sqlite3.Row:
    conn = _get_connection()
    return conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()


def create_user(username: str, password: str):
    conn = _get_connection()
    hashed = _hash(password)

    try:
        with conn:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hashed)
            )
        return get_user(username), "created"

    except Exception as e:
        st.error(f"Error creating user: {e}")
        return None, "error"


def get_or_create_user(username: str, password: str):
    user = get_user(username)

    if user is None:
        # New user — register them
        return create_user(username, password)

    elif user["password_hash"] == _hash(password):
        # Existing user — correct password
        return user, "login"

    else:
        # Existing user — wrong password
        return None, "wrong_password"


def add_exercise(user_id, exercise_name, reps, sets, time):
    conn = _get_connection()

    with conn:
        existing = conn.execute("""
            SELECT * FROM exercises 
            WHERE user_id = ? AND exercise_name = ? AND Date('created_at') = Date('now')
        """, (user_id, exercise_name)).fetchone()

        if existing:
            conn.execute("""
                UPDATE exercises 
                SET reps = reps + ?, sets = sets + ?, time = time + ?
                WHERE id = ?
            """, (reps, sets, time, existing['id']))
        else:
            conn.execute("""
                INSERT INTO exercises (user_id, exercise_name, sets, reps, time)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, exercise_name, sets, reps, time))


def get_users_exercises(user_id):
    conn = _get_connection()

    return conn.execute("""
        SELECT * FROM exercises 
        WHERE user_id = ?
    """, (user_id,)).fetchall()
