import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "data" / "smart_agriculture.db"))


@contextmanager
def connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    database = sqlite3.connect(DATABASE_PATH)
    database.row_factory = sqlite3.Row
    try:
        yield database
        database.commit()
    finally:
        database.close()


def init_database():
    with connection() as database:
        database.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'farmer',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                prediction_type TEXT NOT NULL,
                crop TEXT,
                disease_class INTEGER,
                disease_label TEXT,
                confidence REAL,
                yield_prediction REAL,
                input_data TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        columns = {row["name"] for row in database.execute("PRAGMA table_info(prediction_history)")}
        if "disease_label" not in columns:
            database.execute("ALTER TABLE prediction_history ADD COLUMN disease_label TEXT")


def create_user(name, email, password, role="farmer"):
    with connection() as database:
        cursor = database.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (name.strip(), email.strip().lower(), generate_password_hash(password), role),
        )
        return cursor.lastrowid


def find_user_by_email(email):
    with connection() as database:
        return database.execute(
            "SELECT * FROM users WHERE email = ?", (email.strip().lower(),)
        ).fetchone()


def find_user(user_id):
    with connection() as database:
        return database.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def authenticate_user(email, password):
    user = find_user_by_email(email)
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def add_prediction(user_id, prediction_type, input_data, crop=None, disease_class=None, disease_label=None, confidence=None, yield_prediction=None):
    import json

    with connection() as database:
        cursor = database.execute(
            """
            INSERT INTO prediction_history
                (user_id, prediction_type, crop, disease_class, disease_label, confidence, yield_prediction, input_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, prediction_type, crop, disease_class, disease_label, confidence, yield_prediction, json.dumps(input_data)),
        )
        return cursor.lastrowid


def list_predictions(user_id=None, limit=100):
    with connection() as database:
        if user_id is None:
            return database.execute(
                "SELECT p.*, u.name, u.email FROM prediction_history p LEFT JOIN users u ON u.id = p.user_id ORDER BY p.id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return database.execute(
            "SELECT p.*, u.name, u.email FROM prediction_history p LEFT JOIN users u ON u.id = p.user_id WHERE p.user_id = ? ORDER BY p.id DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()


def list_users():
    with connection() as database:
        return database.execute(
            "SELECT id, name, email, role, created_at FROM users ORDER BY id"
        ).fetchall()


def count_records(table):
    if table not in {"users", "prediction_history"}:
        raise ValueError("Unsupported table")
    with connection() as database:
        return database.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()["total"]


def prediction_summary():
    with connection() as database:
        return database.execute(
            """
            SELECT prediction_type,
                   COUNT(*) AS total,
                   AVG(confidence) AS average_confidence,
                   AVG(yield_prediction) AS average_yield
            FROM prediction_history
            GROUP BY prediction_type
            """
        ).fetchall()
