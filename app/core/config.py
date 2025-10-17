import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- database
    database_url: str

    # We set default values here on purpose, but they should be overridden
    # by environment variables, specially the oauth configuration.
    # They are required for migration to run properly in its own container.

    # TODO: Improve this setup to avoid hardcoding secrets in code.

    # --- auth
    oauth_hash_key: str = (
        "7bdb4bcf0b01f00ca206693965b29145611d9419563630525dc848024c38fc08"
    )
    oauth_algorithm: str = "HS256"
    oauth_token_ttl: int = 30  # in minutes

    # --- pagination
    default_page_size: int = 5
    max_page_size: int = 20

    class Config:
        env_file = (".env",) if os.path.exists(".env") else None

        extra = "ignore"  # Ignore other env variables found in the .env file


settings = Settings()
