# Spec: Registration

## Overview
Implements account creation for Spendly. Currently `/register` only renders the form on GET; there is no POST handling, so new users cannot actually sign up. This step adds server-side validation, duplicate-email checking, password hashing, and user creation, then logs the new user in and redirects to the dashboard — mirroring the pattern already used by the implemented `/login` route.

## Depends on
- Step 1 (Database setup) — `users` table and `get_db()`/`init_db()`/`seed_db()` already implemented in `database/db.py`.

## Routes
- `GET /register` — render the registration form (already implemented, unchanged) — public
- `POST /register` — validate input, create the user, start a session, redirect to `/dashboard` — public

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email` UNIQUE, `password_hash`, `created_at`) already supports registration; the `email` UNIQUE constraint enforces no duplicate accounts.

## Templates
- **Create:** none
- **Modify:** none — `templates/register.html` already POSTs to `/register` and renders an `{% if error %}` block; no template changes are required.

## Files to change
- `app.py` — add POST handling to the existing `register()` view:
  - Read `name`, `email`, `password` from `request.form`, `.strip()` name/email
  - Validate all fields are non-empty and password is at least 8 characters (matches the form's placeholder hint); re-render `register.html` with `error` set on failure
  - Check for an existing user with that email; re-render with `error="An account with this email already exists"` if found
  - Hash the password with `generate_password_hash` (import from `werkzeug.security`, alongside the existing `check_password_hash` import)
  - Insert the new user via a parameterized `INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)`
  - Set `session["user_id"]` and `session["user_name"]` for the new user, then `redirect(url_for("dashboard"))`

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Follow the existing `/login` route's structure and style (connection open/query/close per request, same session keys)

## Definition of done
- [ ] Submitting the register form with a new name/email/password creates a row in `users` with a hashed (not plaintext) password
- [ ] After successful registration, the user is redirected to `/dashboard` and is logged in (session contains `user_id`/`user_name`)
- [ ] Submitting with an email that already exists (e.g. `demo@spendly.com`) re-renders `register.html` with an error and does not create a duplicate row
- [ ] Submitting with a missing field or a password under 8 characters re-renders `register.html` with an error and does not create a user
- [ ] A newly registered user can log out and log back in with the same credentials via `/login`
