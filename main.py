
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pymongo import MongoClient
import os
from database.models.postgres_models import Base
from dotenv import load_dotenv  # Import load_dotenv
load_dotenv()  # Load environment variables from .env file

db_user = os.environ.get("POSTGRES_USER")
db_password = os.environ.get("POSTGRES_PASSWORD")
db = os.environ.get("POSTGRES_DB")

# Database configuration
postgres_url: str = "postgresql://{db_user}:{db_password}@localhost/{db}"
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")

# PostgreSQL setup
engine = create_engine(postgres_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# MongoDB setup
mongo_client = MongoClient(MONGODB_URL)
mongo_db = mongo_client.apprentice_hub

app = FastAPI(
    title="Apprentice Hub Backend",
    description="A centralized platform for managing AI apprenticeship learning and evidence",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get PostgreSQL database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get MongoDB database
def get_mongo_db():
    return mongo_db

@app.get("/")
def read_root():
    return {
        "message": "Apprentice Hub Backend", 
        "version": "1.0.0",
        "status": "MVP Development"
    }

# Include API routers
from api.routers import ksbs, evidence, dashboard

app.include_router(ksbs.router, prefix="/api")
app.include_router(evidence.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "postgres": "connected",
        "mongodb": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
