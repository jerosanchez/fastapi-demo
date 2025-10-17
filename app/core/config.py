import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- database
    database_url: str

    # --- auth
    oauth_hash_key: str
    oauth_algorithm: str
    oauth_token_ttl: int  # in minutes

    # --- pagination
    default_page_size: int
    max_page_size: int

    class Config:
        # Load variables from a .env file in the same folder
        # Remember to copy `.env.example` into `.env` and adjust values
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


settings = Settings()
