from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.users.models import User


class AuthRepositoryABC(ABC):
    @abstractmethod
    def get_user_by_email(self, db: Session, email: str) -> User | None:
        pass


class AuthRepository(AuthRepositoryABC):
    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()
