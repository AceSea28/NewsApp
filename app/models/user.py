# SQLAlchemy model class representing the user schema, including fields and relationships.

from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import Enum as SqlEnum

class UserRole(str, enum.Enum):
    admin= "admin"
    user= "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    role= Column(SqlEnum(UserRole), default= UserRole.user, nullable=False)