# Spec: Profile Page

## Overview
This feature implements a view-only profile page for logged-in users. It converts the `/profile` stub into a real route that shows the current user's account details (name, email, member-since date) and a summary of their expense activity (total spent, number of expenses). No editing capability is introduced at this stage — this is a read-only account summary, giving users a place to see their identity and activity at a glance before any account-editing or settings features exist.

## Depends on
- Step 01 — Database Setup (`users` and `expenses` tables must exist)
- Step 02 — Registration (a user must exist to have a profile)
- Step 03 — Login and Logout (`session["user_id"]` must be set to identify the current user)

## Routes
- `GET /profile` — render the current user's profile with account details and expense summary — logged-in only (redirect to `/login` if no session)

## Database changes
No database changes. The `users` table (Step 01) already stores `name`, `email`, and `created_at`. The `expenses` table already stores `amount` and `user_id`, which is enough to compute a summary.

## Templates
- **Create:** `templates/profile.html` — displays name, email, member-since date, total spent, and expense count
- **Modify:** `templates/base.html` — add a "Profile" link next to "Dashboard" in the logged-in nav links block

## Files to change
- `app.py` — implement `profile()`: require login, fetch the user record and expense summary, render `profile.html`
- `database/db.py` — add `get_user_by_id(user_id)` helper returning `id`, `name`, `email`, `created_at` (or `None`)
- `templates/base.html` — add profile nav link

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use f-strings in SQL
- Passwords hashed with werkzeug (no change needed here, but never select or display `password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode paths
- `get_user_by_id` belongs in `database/db.py`, not inline in the route
- If `session["user_id"]` is missing, redirect to `url_for("login")` (same pattern as `dashboard()`)
- Compute total spent and expense count in the route using data already queryable from `expenses` — do not add a new table or column for it
- The `/profile` route must not return the raw stub string

## Definition of done
- [ ] Visiting `GET /profile` while logged out redirects to `/login`
- [ ] Visiting `GET /profile` while logged in (e.g. demo@spendly.com / demo123) renders the profile page
- [ ] The profile page shows the user's name, email, and member-since date
- [ ] The profile page shows total amount spent and number of expenses, matching the values shown on `/dashboard`
- [ ] The nav bar shows a "Profile" link when logged in, and it links to `/profile`
- [ ] The `/profile` route no longer returns the raw stub string
