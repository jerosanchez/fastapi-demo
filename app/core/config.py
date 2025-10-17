import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- database
    database_url: str

    # --- auth
    oauth_hash_key: str
    oauth_algorithm: str
    oauth_token_ttl: int

    # --- pagination
    default_page_size: int
    max_page_size: int

    class Config:
        env_file = (".env",) if os.path.exists(".env") else None

        extra = "ignore"  # Ignore other env variables found in the .env file


settings = Settings()
