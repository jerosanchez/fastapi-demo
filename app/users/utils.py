from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# No need to encapsulate in a class since there is no state;
# if we change the implementation later, we can do so here directly.
# Remember to keep this in sync with app/auth/utils.py
# Kept separate for clarity of concerns and to allow microservice separation.
def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)
