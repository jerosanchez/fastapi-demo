from pydantic import BaseModel, EmailStr


# Not used any longer in favor of form params
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None
