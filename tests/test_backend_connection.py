from datetime import datetime

from database.queries import (
    get_category_breakdown,
    get_recent_transactions,
    get_summary_stats,
    get_user_by_id,
)

# --- get_user_by_id -------------------------------------------------- #


def test_get_user_by_id_valid_user(seed_user_id):
    result = get_user_by_id(seed_user_id)
    assert result["name"] == "Demo User"
    assert result["email"] == "demo@spendly.com"
    assert result["member_since"] == datetime.now().strftime("%B %Y")


def test_get_user_by_id_nonexistent():
    assert get_user_by_id(999999) is None


# --- get_summary_stats ------------------------------------------------ #


def test_get_summary_stats_with_expenses(seed_user_id):
    stats = get_summary_stats(seed_user_id)
    assert round(stats["total_spent"], 2) == 355.49
    assert stats["transaction_count"] == 8
    assert stats["top_category"] == "Bills"


def test_get_summary_stats_no_expenses(empty_user_id):
    assert get_summary_stats(empty_user_id) == {
        "total_spent": 0,
        "transaction_count": 0,
        "top_category": "—",
    }


# --- get_recent_transactions ------------------------------------------ #


def test_get_recent_transactions_with_expenses(seed_user_id):
    txns = get_recent_transactions(seed_user_id)
    assert len(txns) == 8
    dates = [t["date"] for t in txns]
    assert dates == sorted(dates, reverse=True)
    for t in txns:
        assert set(t.keys()) >= {"date", "description", "category", "amount"}


def test_get_recent_transactions_no_expenses(empty_user_id):
    assert get_recent_transactions(empty_user_id) == []


# --- get_category_breakdown -------------------------------------------- #


def test_get_category_breakdown_with_expenses(seed_user_id):
    breakdown = get_category_breakdown(seed_user_id)
    amounts = [item["amount"] for item in breakdown]
    assert amounts == sorted(amounts, reverse=True)
    assert sum(item["pct"] for item in breakdown) == 100
    assert all(isinstance(item["pct"], int) for item in breakdown)


def test_get_category_breakdown_no_expenses(empty_user_id):
    assert get_category_breakdown(empty_user_id) == []


# --- routes ------------------------------------------------------------ #


def test_profile_redirects_when_not_logged_in(client):
    response = client.get("/profile")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_profile_authenticated_seed_user(client):
    client.post("/login", data={"email": "demo@spendly.com", "password": "demo123"})
    response = client.get("/profile")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Demo User" in body
    assert "demo@spendly.com" in body
    assert "₹" in body
    assert "355.49" in body
    assert "Bills" in body

    assert body.index("Lunch with friends") < body.index("Groceries")

    for category in (
        "Bills",
        "Shopping",
        "Health",
        "Food",
        "Entertainment",
        "Transport",
        "Other",
    ):
        assert category in body


def test_profile_fresh_user_no_expenses(client):
    client.post(
        "/register",
        data={
            "name": "Fresh User",
            "email": "fresh-user@example.com",
            "password": "password123",
        },
    )
    response = client.get("/profile")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "₹0.00" in body
