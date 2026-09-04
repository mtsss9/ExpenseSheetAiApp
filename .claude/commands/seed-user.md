---
description: Create a test user (with sample expenses) in the local SQLite dev database
argument-hint: [name] [email] [password]
---

Create a new test user directly in `expense_tracker.db` for local development/testing. This is separate from the fixed "Demo User" that `seed_db()` in `database/db.py` creates on first run — use this command whenever you need an *additional* user (e.g. to test multi-user isolation, login flows, or empty-state screens).

Arguments (`$ARGUMENTS`, all optional, space-separated — name may be multiple words if email/password are also given):
- name — defaults to `Test User`
- email — defaults to `test+<random 4 hex chars>@spendly.com` so repeated runs don't collide
- password — defaults to `test1234`

Steps:

1. Make sure the schema exists: call `init_db()` from `database/db.py` (safe to call repeatedly, uses `CREATE TABLE IF NOT EXISTS`).
2. Resolve the name/email/password from `$ARGUMENTS`, falling back to the defaults above.
3. Using `get_db()`, check whether a user with that email already exists.
   - If it does, stop and report the conflict — do not overwrite or duplicate. Suggest passing a different email.
4. Hash the password with `werkzeug.security.generate_password_hash` and insert the new row into `users`.
5. Insert 3–5 sample expenses for the new user, picked from the fixed category list (Food, Transport, Bills, Health, Entertainment, Shopping, Other), with dates in the current month (`YYYY-MM-DD`) and small realistic amounts/descriptions. Vary them from the existing demo user's seed data so they're easy to tell apart.
6. Use parameterized queries only (no string-formatted SQL), and `conn.commit()` / `conn.close()` when done.
7. Report back: the user's id, name, email, the plaintext password (since it was just set), and how many expenses were inserted.

Do this by running a short one-off Python snippet against `database/db.py`'s helpers (or a small temp script) rather than editing `seed_db()` itself — `seed_db()` must stay limited to the single fixed demo user so it remains idempotent and predictable for the guided exercise.
