from uuid import UUID

from pydantic import BaseModel, field_validator


class VotePost(BaseModel):
    post_id: UUID
    vote_direction: int

    @field_validator("vote_direction")
    def validate_vote_direction(cls, value):
        if value not in (0, 1):
            raise ValueError("vote_direction must be 0 or 1")
        return value
