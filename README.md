
# FastAPI CRUD User API

A REST API built with FastAPI, SQLAlchemy, and SQLite. It supports full CRUD operations for users, automatic database seeding, and a simple password intake endpoint for frontend integration.

## Live Demo

- Base URL: https://ekhsan-fastapi.onrender.com
- Swagger UI: https://ekhsan-fastapi.onrender.com/docs
- ReDoc: https://ekhsan-fastapi.onrender.com/redoc

## Features

- Create, read, update, and delete users
- Automatic seed data on first startup
- Pydantic validation for request and response payloads
- SQLite by default, with `DATABASE_URL` support for other databases
- CORS configuration through environment variables
- `/passwords` endpoint for frontend-to-backend integration testing

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

## API Endpoints

### `GET /`
Returns a simple welcome message.

### `GET /users`
Returns all users.

### `GET /users/{user_id}`
Returns one user by ID.

### `POST /users`
Creates a new user.

Example body:

```json
{
   "name": "Jane",
   "role": "Analyst"
}
```

### `PUT /users/{user_id}`
Updates an existing user.

Example body:

```json
{
   "name": "Jane Doe",
   "role": "Senior Analyst"
}
```

### `DELETE /users/{user_id}`
Deletes a user by ID.

### `POST /passwords`
Accepts a password payload and logs it on the server.

Example body:

```json
{
   "password": "MySecurePassword123!"
}
```

## Local Setup

1. Clone the repository.

```bash
git clone https://github.com/EkhsanFitri94/fastapi-crud-api.git
cd fastapi-crud-api
```

2. Create and activate a virtual environment if you want one.

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Start the API.

```bash
uvicorn main:app --reload
```

5. Open the docs in your browser at `http://127.0.0.1:8000/docs`.

## Environment Variables

- `DATABASE_URL`: optional database connection string. Defaults to `sqlite:///./database.db`
- `CORS_ORIGINS`: optional comma-separated list of allowed origins. Defaults to `*`

Example:

```bash
DATABASE_URL=sqlite:///./database.db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5500
```

## Deployment

The project includes Render configuration in `render.yaml` and a startup script in `render.sh`.

## Project Structure

```text
.
├── main.py
├── README.md
├── render.sh
├── render.yaml
├── requirements.txt
└── .gitignore
```

## Notes

- The database is seeded automatically when the app starts and the user table is empty.
- The app returns structured validation and not-found responses through FastAPI and Pydantic.
