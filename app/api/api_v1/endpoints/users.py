# Defines API routes and logic for user-related operations.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user
from app.db.session import get_db
from app.core.security import create_access_token, verify_password
from jose import JWTError
from app.core.dependencies import get_current_user, get_current_admin_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/admin-only", response_model=UserResponse)
def read_admin_data(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return current_user