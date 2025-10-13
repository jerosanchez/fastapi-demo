from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserSchemaBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserOut(UserSchemaBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(UserSchemaBase):
    password: str
