# 💰 Finance App

A personal finance management application built with FastAPI, PostgreSQL, JWT authentication, Docker, and a clean dark-mode frontend.

---

## Features

- User registration and login with JWT authentication
- Create, list, update and delete financial transactions
- Income and expense tracking with categories
- Monthly summary with total income, expenses and balance
- Clean dark-mode frontend interface
- Fully containerized with Docker

---

## Tech Stack

**Backend:** Python 3.11, FastAPI, PostgreSQL, SQLAlchemy, JWT, Docker

**Frontend:** HTML, CSS, JavaScript (vanilla)

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /auth/register | Register a new user | No |
| POST | /auth/login | Login and get JWT token | No |
| GET | /transactions/ | List all transactions | Yes |
| POST | /transactions/ | Create a transaction | Yes |
| PUT | /transactions/{id} | Update a transaction | Yes |
| DELETE | /transactions/{id} | Delete a transaction | Yes |
| GET | /transactions/summary | Get monthly summary | Yes |

---

## Running Locally

Requirements: Docker and Docker Compose

1. Clone the repository
2. Create a .env file with DATABASE_URL, SECRET_KEY, ALGORITHM and ACCESS_TOKEN_EXPIRE_MINUTES
3. Run docker compose up --build
4. Open http://localhost:8000

API docs at http://localhost:8000/docs

---

## Author

Giann Luca Neme Battistutta
GitHub: github.com/GiannBattistutta
LinkedIn: linkedin.com/in/giannlucaneme
