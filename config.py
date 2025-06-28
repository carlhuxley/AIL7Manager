
# config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    postgres_user: str = os.environ.get("POSTGRES_USER")
    postgres_password: str = os.environ.get("POSTGRES_PASSWORD")
    postgres_host: str = os.environ.get("POSTGRES_HOST", "127.0.0.1")
    postgres_port: str = os.environ.get("POSTGRES_PORT", "5432")
    postgres_db: str = os.environ.get("POSTGRES_DB")

    @property
    def postgres_url(self):
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    mongodb_url: str = "mongodb://localhost:27017/"

    # Security settings
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Application settings
    app_name: str = "Apprentice Hub"
    app_version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

