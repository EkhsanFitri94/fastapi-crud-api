import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import (
    Session,
    declarative_base,
    sessionmaker,
)

# --- 1. DATABASE SETUP ---
# This creates a file called 'database.db' in your folder
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- 2. DATABASE MODEL ---
# This replaces our fake dictionary.
# It tells the database exactly what a "User" looks like.
class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)


# Actually create the database.db file and the users table
Base.metadata.create_all(bind=engine)


# --- 3. PYDANTIC SCHEMAS (Data Validation) ---
# These stay exactly the same!
# FastAPI still needs to know what data to accept/return.
class UserCreate(BaseModel):
    name: str
    role: str


class User(UserCreate):
    id: int


class MessageResponse(BaseModel):
    message: str


class UserResponse(BaseModel):
    data: User


class UsersResponse(BaseModel):
    data: list[User]


class ErrorResponse(BaseModel):
    detail: str


class PasswordCreate(BaseModel):
    password: str


# --- 4. DEPENDENCY ---
# This function opens a connection to the database,
# yields it to our endpoint, then closes it.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- 5. FASTAPI APP & ENDPOINTS ---
app = FastAPI()

cors_origins = os.getenv("CORS_ORIGINS", "*").strip()
allow_origins = (
    ["*"]
    if cors_origins == "*"
    else [origin.strip() for origin in cors_origins.split(",") if origin.strip()]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def seed_users_if_empty():
    db = SessionLocal()
    try:
        existing_count = db.query(DBUser).count()
        if existing_count == 0:
            db.add_all(
                [
                    DBUser(name="Ekhsan", role="Developer"),
                    DBUser(name="Alice", role="Designer"),
                    DBUser(name="Bob", role="Manager"),
                ]
            )
            db.commit()
    finally:
        db.close()


@app.get("/", response_model=MessageResponse)
def read_root():
    return {"message": "Welcome to my first REAL database API!"}


@app.get("/users", response_model=UsersResponse)
def get_users(db: Session = Depends(get_db)):
    # .all() is SQLAlchemy's way of saying "SELECT * FROM users"
    users = db.query(DBUser).all()
    return {"data": users}


@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # .filter() and .first() replace our old for-loop
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user}


@app.post("/users", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Create a new DBUser object
    db_user = DBUser(name=user.name, role=user.role)

    # Add it to the database session
    db.add(db_user)

    # Actually save it to the hard drive
    db.commit()

    # Refresh to get the auto-generated ID from the database
    db.refresh(db_user)

    return {"data": db_user}


@app.put(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={404: {"model": ErrorResponse}},
)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the fields
    db_user.name = user.name
    db_user.role = user.role

    # Save changes to hard drive
    db.commit()
    db.refresh(db_user)

    return {"data": db_user}


@app.delete(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={404: {"model": ErrorResponse}},
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete from database
    db.delete(db_user)

    # Save changes to hard drive
    db.commit()

    return {"data": db_user}


@app.post("/passwords", status_code=201)
def save_password(payload: PasswordCreate, db: Session = Depends(get_db)):
    # For now, we just print it to the server logs to prove we got it
    print(f"Received password from frontend: {payload.password}")
    return {"message": "Password received and logged!"}
