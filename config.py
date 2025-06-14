
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    postgres_url: str = "postgresql://user:password@localhost/apprentice_hub"
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
