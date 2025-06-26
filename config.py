
import os
from pydantic_settings import BaseSettings

db_user = os.environ.get("POSTGRES_USER")
db_password = os.environ.get("POSTGRES_PASSWORD")
db = os.environ.get("POSTGRES_DB")

class Settings(BaseSettings):
    # Database settings
    postgres_url: str = "postgresql://{db_user}:{db_password}@127.0.0.1:5432/{db}"
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
