from sqlalchemy import Column, ForeignKey, String

from app.core.database import Base


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(
        String, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
