"""Pure data-access helpers for the profile page.

No Flask imports — each function takes primitive args, returns plain
dicts/lists, calls get_db() internally, and closes the connection
before returning.
"""

from datetime import datetime

from database.db import get_db


def get_user_by_id(user_id):
    conn = get_db()
    row = conn.execute(
        "SELECT name, email, created_at FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()

    if row is None:
        return None

    created_at = datetime.strptime(row["created_at"][:10], "%Y-%m-%d")
    return {
        "name": row["name"],
        "email": row["email"],
        "member_since": created_at.strftime("%B %Y"),
    }


def get_summary_stats(user_id):
    """Return {'total_spent', 'transaction_count', 'top_category'}.
    Zero-expense users get {'total_spent': 0, 'transaction_count': 0,
    'top_category': '—'}."""
    # TODO(subagent: summary-stats)
    raise NotImplementedError


def get_recent_transactions(user_id, limit=10):
    """Return [{'date','description','category','amount'}, ...],
    newest-first. Zero-expense users get []."""
    # TODO(subagent: transaction-history)
    raise NotImplementedError


def get_category_breakdown(user_id):
    """Return [{'name','amount','pct'}, ...] ordered by amount desc.
    pct values are ints summing to exactly 100 (largest category
    absorbs the rounding remainder). Zero-expense users get []."""
    # TODO(subagent: category-breakdown)
    raise NotImplementedError
