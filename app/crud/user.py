#  CRUD operations related to user data.

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, 
                   email=user.email, 
                   hashed_password=get_password_hash(user.password),
                   role= user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
