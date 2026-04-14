
```markdown
# ⚡ FastAPI CRUD User API

A robust, production-ready RESTful API built with FastAPI and SQLAlchemy. Features full CRUD operations, automatic database seeding, and proper data validation.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Deployed-brightgreen)

## 🌐 Live Base URL
[https://ekhsan-fastapi.onrender.com](https://ekhsan-fastapi.onrender.com)

## 📖 Interactive Documentation
FastAPI auto-generates docs. You can test all endpoints directly in your browser:
* **Swagger UI:** [https://ekhsan-fastapi.onrender.com/docs](https://ekhsan-fastapi.onrender.com/docs)
* **ReDoc:** [https://ekhsan-fastapi.onrender.com/redoc](https://ekhsan-fastapi.onrender.com/redoc)

## 🧩 Architecture & Features
* **Database:** Uses SQLAlchemy ORM with SQLite for persistent data storage.
* **Pydantic Schemas:** Strict data validation for incoming requests and outgoing responses.
* **Auto-Seeding:** Automatically populates the database with default users on the first startup.
* **Error Handling:** Proper HTTP 404 responses with structured error models.
* **Integration:** Includes a `/passwords` endpoint designed to receive data from the Password Generator frontend.

## 🛠️ How to run locally
1. Clone the repository:
   ```bash
   git clone https://github.com/EkhsanFitri94/fastapi-crud-api.git

2. Install dependencies:
pip install -r requirements.txt

3. Run the server:
uvicorn main:app --reload
