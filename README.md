# CPS420 - Mid-Term Programming Assignment

## FastAPI Chapters 1–9: Campus Lost & Found API with SQLite & SQLAlchemy

You will complete a **Campus Lost & Found REST API** that allows students to report lost items and submit claim requests in a **SQLite database** via **SQLAlchemy ORM**. The database setup, models, and some routes are already provided — your job is to fill in the missing logic marked with `# TODO`.

### Project Structure

```bash
lostandfound_api/
├── database.py       # PROVIDED — SQLAlchemy engine & session setup
├── models.py         # PROVIDED — SQLAlchemy ORM models
├── schemas.py        # PROVIDED — Pydantic schemas
├── crud.py           # PARTIALLY PROVIDED — you complete the missing functions
├── main.py           # PARTIALLY PROVIDED — you complete the missing routes
└── README.md
```

### Getting Started

1. **Install dependencies:**
```bash
pip install fastapi uvicorn sqlalchemy
```

2. **Run the server:**
```bash
uvicorn main:app --reload
```

3. **Visit the interactive API docs:**
```
http://127.0.0.1:8000/docs
```

All provided routes work immediately, so you can confirm your database is set up before writing any code.

### Your Tasks

Complete the 10 TODOs marked in `crud.py` and `main.py`. Each TODO is worth 10 points (100 total).

| # | Location | What to Implement | Points |
| :-- | :-- | :-- | :-- |
| TODO #1 | `crud.py` | `create_item()` | 10 |
| TODO #2 | `crud.py` | `update_item()` | 10 |
| TODO #3 | `crud.py` | `delete_item()` (with cascade) | 10 |
| TODO #4 | `crud.py` | `create_claim()` | 10 |
| TODO #5 | `crud.py` | `get_unresolved_items()` — filtered query | 10 |
| TODO #6 | `crud.py` | `get_item_stats()` — aggregate query | 10 |
| TODO #7 | `main.py` | `POST /item` route | 10 |
| TODO #8 | `main.py` | `PUT /item/{item_id}` route | 10 |
| TODO #9 | `main.py` | `DELETE /item/{item_id}` route | 10 |
| TODO #10 | `main.py` | `GET /item/unresolved` route | 10 |

### Tips

- **Route order matters:** The comment in TODO #10 reminds you to place `GET /item/unresolved` **above** `GET /item/{item_id}` in the final file — FastAPI matches routes top-to-bottom and would otherwise treat `"unresolved"` as an integer ID
- The `POST /item/{item_id}/claim` route is fully provided — but it **depends on your TODO #4** (`create_claim()`) to work correctly, so make sure that is implemented first
- For TODO #6, `func.count()` returns `0` rather than `None` when there are no claims, so `ItemStats` will always have valid integers — no need for `Optional` fields

### Grading

Your solution will be graded based on:
- Correct implementation of all 10 TODOs
- Proper error handling and HTTP status codes
- Adherence to the provided hints and best practices
- Code clarity and organization

Good luck!