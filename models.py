import uuid

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP

from database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE")
    rating = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default="now()")


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default="now()")
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
