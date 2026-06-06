# Macro Track

Macro Track is a backend API for tracking nutrition and meals. It supports user registration and authentication, product management, meal creation, and daily diary entries. The application is built as a REST API using FastAPI.

## Project Overview

Macro Track is focused on managing richer database relationships rather than just flat resources. The app models users, owned and public products, meals composed of multiple product entries, and a diary of meal consumption.

The core data relationships are:

- `User` owns `Product` records and `Meal` records.
- `Meal` is a container for `MealProduct` items, each linking to a `Product` and recording the grams consumed.
- `UserDiary` records tie a `User` to a `Meal` at a specific timestamp.
- Public products are allowed by keeping `Product.user_id` nullable, enabling shared items alongside user-owned products.

This design supports cascading deletes and authorization checks while preserving a clear separation between user-owned data and shared resources.

## Requirements

- Python 3.12
- PostgreSQL database
- Docker and Docker Compose (optional, for local PostgreSQL)
- `.env` file with at least:
  - `SECRET_KEY`
  - `ALGORITHM`

## Used Technologies

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- JWT
- python-dotenv
- PostgreSQL
- Docker Compose
- uvicorn
- pytest

## Instructions to Open and Run the Project

1. Activate the virtual environment:

```bash
source env/bin/activate
```

2. Start PostgreSQL locally with Docker Compose (recommended):

```bash
docker compose up -d
```

3. Create a `.env` file in the project root with your JWT settings, for example:

```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

4. Apply database migrations if you want to keep schema history consistent:

```bash
./env/bin/alembic upgrade head
```

5. Start the FastAPI server:

```bash
./env/bin/uvicorn main:app --reload
```

6. Open the API documentation in your browser:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

Run the test suite with:

```bash
./env/bin/pytest -q
```

## Additional Notes

- The test suite uses an in-memory SQLite database, so it does not require PostgreSQL during testing.
- The main application uses PostgreSQL, matching the Docker Compose service credentials:
  - `POSTGRES_USER=macro_track_user`
  - `POSTGRES_PASSWORD=macro_track_passwd`
  - `POSTGRES_DB=macro_track_db`