import os
import tempfile

import pytest

_db_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.close(_db_fd)
os.environ["EXPENSE_TRACKER_DB_PATH"] = _db_path

from app import app as flask_app  # noqa: E402
from database.db import get_db  # noqa: E402
from werkzeug.security import generate_password_hash  # noqa: E402


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as test_client:
        yield test_client


@pytest.fixture()
def seed_user_id():
    conn = get_db()
    row = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()
    conn.close()
    return row["id"]


@pytest.fixture(scope="session")
def empty_user_id():
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("No Expenses", "no-expenses@example.com", generate_password_hash("password123")),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id
