# Spec: Profile Page Polish Pass

## Overview
This is a UI-only follow-up to Step 4 (profile page). The profile page (`templates/profile.html`) already meets every item in `04-profile-page.md`'s Definition of Done, but three presentation gaps remain: it has no responsive behaviour of its own (it clips instead of reflowing below ~768px), money figures don't use tabular numerals (so digits misalign across rows), and every category badge renders in the same single accent colour regardless of category. This step closes those gaps with CSS and markup changes only — no routes, data, or auth logic change.

## Depends on
- Step 4: Profile page (must be complete — user info card, stats, transaction table, and category breakdown must already exist)

## Routes
No new routes. `GET /profile` is unchanged.

## Database changes
No database changes.

## Templates
- **Modify:** `templates/profile.html` — update the category badge markup in the transaction table loop to select a per-category modifier class (e.g. `category-pill category-pill--{{ transaction.category|lower }}`) instead of the single static `category-pill` class. No other markup changes.

## Files to change
- `templates/profile.html` — category pill markup (see above)
- `static/css/style.css` — profile section only (currently lines ~755-865):
  1. Add responsive rules for `.profile-card`, `.profile-stats` / `.stat-tile`, `.breakdown-row`, and `.expense-table-wrap`, using a `max-width: 768px` breakpoint consistent with the existing `900px` / `600px` pattern already in the Responsive block:
     - `.profile-card` stacks avatar above name/email/member-since instead of sitting side by side
     - `.stat-tile` items go full-width (stack vertically) instead of `flex: 1 1 200px` wrapping awkwardly
     - `.breakdown-row`'s fixed `grid-template-columns: 140px 1fr 90px` collapses to a stacked layout (label, then bar, then value) so long category names and the progress bar aren't squeezed
     - `.expense-table-wrap` changes from `overflow: hidden` to `overflow-x: auto` so the transaction table scrolls horizontally instead of clipping columns
  2. Add `font-variant-numeric: tabular-nums;` to `.stat-value`, `.amount-col`, and `.breakdown-value`
  3. Add category-specific CSS custom properties to `:root` (e.g. `--cat-food`, `--cat-bills`, `--cat-transport`, `--cat-health`, `--cat-entertainment`, `--cat-shopping`, `--cat-other` — covering every category used in `database/db.py`'s seed data and `profile.html`'s hardcoded rows) and add matching `.category-pill--<category>` modifier classes that set `background`/`color` from those variables, following the same two-tone pattern as the existing `.category-pill` (light background, saturated text)

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (not applicable — no queries in this step)
- Passwords hashed with werkzeug (not applicable — no auth changes)
- Use CSS variables — never hardcode hex values; category colours must be defined once in `:root` and referenced via `var(--cat-...)`, not inlined
- All templates extend `base.html` (already true; no change to this)
- No inline styles — category selection happens via a Jinja-computed class name, never a `style="..."` attribute
- Do not touch `base.html`, `app.py` routes/logic, `database/db.py`, or any file outside `templates/profile.html` and the profile section of `static/css/style.css`
- Do not introduce an icon library or any new font/CDN dependency
- Keep the existing `--font-display` / `--font-body` / spacing tokens; don't invent a new type or spacing scale

## Definition of done
- [ ] At a viewport width ≤ 768px, the profile avatar/name/email block stacks vertically instead of overflowing
- [ ] At ≤ 768px, the three stat tiles stack to full width and remain readable (no clipped text)
- [ ] At ≤ 768px, each category breakdown row stacks its label, bar, and value instead of squeezing into three fixed columns
- [ ] At ≤ 768px, the transaction table scrolls horizontally (via touch/drag or a visible scrollbar) instead of clipping columns
- [ ] Stat values, table amounts, and breakdown values render with tabular (fixed-width) numerals — digits in different rows line up in a monospaced-number grid when inspected
- [ ] Each category (`Food`, `Bills`, `Transport`, `Health`, `Entertainment`, `Shopping`, `Other`) renders its pill in a visually distinct colour, not all identical
- [ ] No hex colour values appear in `profile.html` or in the new/changed CSS rules — only `var(--...)` references
- [ ] No inline `style="..."` attributes were added to `profile.html`
- [ ] `/profile` still returns 200 for a logged-in user and still redirects to `/login` when logged out (unchanged behaviour, regression check)
