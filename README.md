# 📊 Macro Track

Macro Track is a backend API for tracking nutrition, meals, and daily food intake.  
It is built as a REST API using FastAPI and focuses on relational data modeling, authentication, and ownership-based access control.

The project is designed to go beyond simple CRUD applications by implementing nested relationships, permission checks, and structured nutrition tracking logic.

---

## 🚀 Key Features

- JWT-based authentication with secure password hashing
- Ownership-based access control (users can only modify their own resources)
- Public vs private products system
- Nested resource creation (Meal → MealProducts → Product)
- Diary tracking with timestamped meal entries
- Relational data model with many-to-many-like structure via join table
- Full test coverage using pytest with isolated in-memory SQLite database
- Clear separation between user-owned and shared data

---

## 🧠 Domain Model Overview

The application models a structured nutrition tracking system:

```text
User
├── Product (owned or public)
├── Meal
│   └── MealProduct (join table linking Meal ↔ Product)
└── UserDiary (Meal + timestamp)
```

### Core relationships

- **User → Product**
  - Users can create private products
  - Products can also be public (`user_id = NULL`)

- **User → Meal**
  - Meals are user-owned containers for food composition

- **Meal → MealProduct → Product**
  - Each meal is composed of multiple products with gram-based quantities

- **UserDiary**
  - Stores when a user consumed a meal (timestamped entries)

---

## 🧱 Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy ORM
- Pydantic
- Alembic
- JWT Authentication (custom implementation)
- PostgreSQL (production)
- SQLite in-memory (testing)
- pytest
- Docker & Docker Compose
- uvicorn

---

## 🔐 Authentication & Authorization

- JWT tokens are used for authentication
- Passwords are hashed before storage
- Endpoints are protected using dependency injection
- Ownership checks prevent access to unauthorized resources
- Public products are accessible without ownership

---

## 📡 API Overview

### Auth

- POST /auth/register — Register a new user (public)
- POST /auth/login — Obtain JWT access token (public)

---

### Users

- GET /users/ — Get current user profile (authenticated)
- PATCH /users/ — Update current user profile (authenticated)

---

### Products

- POST /products/ — Create user-owned product (authenticated)
- GET /products/ — List user + public products (authenticated)
- GET /products/{id} — Get product by id (authenticated + ownership rules)
- DELETE /products/{id} — Delete product (authenticated)

---

### Meals

- POST /meals/ — Create meal with nested products (authenticated)
- PATCH /meals/{id} — Update meal and its composition (authenticated)
- PATCH /meals/is_active/{id} — Toggle meal active state (authenticated)
- DELETE /meals/{id} — Delete meal (authenticated)

---

### Diary

- POST /diary/ — Add meal entry with timestamp (authenticated)
- GET /diary/ — List user diary entries (authenticated)
- GET /diary/{date} — Filter entries by date (authenticated)
- GET /diary/entry/{id} — Get specific diary entry (authenticated)
- PATCH /diary/{id} — Update diary entry (authenticated)
- DELETE /diary/{id} — Delete diary entry (authenticated)

---

## 🧪 Testing Strategy

The project uses `pytest` with:

- In-memory SQLite database for full isolation
- Dependency override for FastAPI database session
- Fixtures for users, products, meals, and authentication tokens
- Clean database state between tests

Run tests:

```bash
pytest -q
```

## ⚙️ Setup & Run

1. Activate the virtual environment:

```bash
source env/bin/activate
```

2. Start PostgreSQL locally with Docker Compose:

```bash
docker compose up -d
```

3. Create a `.env` file in the project root with your JWT settings, for example:

```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

4. Apply database migrations:

```bash
alembic upgrade head
```

5. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Open the API documentation in your browser:

```text
http://127.0.0.1:8000/docs
```

## 🧩 Architecture Notes

- Relational-heavy design instead of flat CRUD resources
- Explicit ownership checks in the service layer
- Nested writes handled in transactions (Meal → MealProducts)
- Separation of public vs private data via nullable foreign keys
- Designed with testability in mind using dependency injection and session overrides

## 🧠 What This Project Demonstrates

- Backend API design with FastAPI
- Relational database modeling (1-N, M-N via join tables)
- Authentication and authorization patterns (JWT + ownership checks)
- Transactional consistency in nested writes
- Test-driven backend development
- Clean separation of concerns using dependency injection