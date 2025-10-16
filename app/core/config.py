import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- database
    db_driver: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

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
        env_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), ".env"
        )


settings = Settings()
