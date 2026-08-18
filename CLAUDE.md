# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a Flask-based personal expense tracker. Users register, log in, and log/edit/delete expense entries backed by SQLite. The project is being built incrementally as a guided, step-by-step exercise — many routes and the database layer are intentionally left as placeholders with `# Step N` comments marking what's not yet implemented.

## Commands

```bash
# Set up (venv already exists at ./venv)
venv\Scripts\activate                 # Windows
pip install -r requirements.txt

# Run the dev server (http://127.0.0.1:5001)
python app.py

# Run tests
pytest
pytest path/to/test_file.py::test_name   # single test
```

There is no build/lint step configured (no linter, no frontend bundler). No test files exist yet; `pytest` and `pytest-flask` are installed in anticipation of them.

## Architecture

- **`app.py`** — single-file Flask app with all routes. Implemented: `/`, `/register`, `/login` (GET, template render only — no form handling/auth logic yet). Stubbed placeholders returning plain text: `/logout` (Step 3), `/profile` (Step 4), `/expenses/add` (Step 7), `/expenses/<id>/edit` (Step 8), `/expenses/<id>/delete` (Step 9). Runs on port 5001 with `debug=True`.
- **`database/db.py`** — not yet implemented. Intended to hold `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (creates tables with `CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample dev data). No schema exists yet. The SQLite file is expected at `expense_tracker.db` (already in `.gitignore`), created at the project root.
- **`templates/`** — Jinja2 templates. `base.html` defines the shared layout (nav, footer, font/CSS links) with `title`, `head`, `content`, and `scripts` blocks; `landing.html`, `login.html`, `register.html` extend it. The login/register forms already POST to `/login` and `/register` and render an `{% if error %}` block, but `app.py` doesn't yet handle POST or set `error` — that logic still needs to be added.
- **`static/`** — `css/style.css` (all styling) and `js/main.js` (currently empty, placeholder for future client-side behavior).
- No auth/session mechanism, ORM, or migrations exist yet — when implementing login/register, sessions/cookies and password hashing will need to be added from scratch.
