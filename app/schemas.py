from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

### Post schemas


class PostSchemaBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


class PostOut(PostSchemaBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class PostCreate(PostSchemaBase):
    pass


class PostUpdate(PostSchemaBase):
    pass


### User schemas


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
