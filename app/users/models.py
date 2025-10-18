import uuid

from sqlalchemy import Boolean, Column, Index, String
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.core.dependencies.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False)  # Removed unique=True
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default="now()")
    is_active = Column(Boolean, server_default="TRUE", nullable=False)

    __table_args__ = (Index("users_email_key", "email", unique=True),)
