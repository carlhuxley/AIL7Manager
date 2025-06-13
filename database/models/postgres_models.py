from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from pymongo import MongoClient

mongo_client = MongoClient('mongodb://localhost:27017/') # This needs to be mocked

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    oauth_provider = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    projects = relationship("Project", back_populates="owner")
    learning_logs = relationship("LearningLog", back_populates="user")

class KSB(Base):
    __tablename__ = "ksbs"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(Text)

    evidence_links = relationship("EvidenceKSBLink", back_populates="ksb")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    due_date = Column(DateTime)
    status = Column(String)

    owner = relationship("User", back_populates="projects")
    evidence = relationship("EvidenceKSBLink", back_populates="project") # Note: this needs refinement as evidence is in Mongo


def get_related_evidence(self):
    db = mongo_client.get_database('your_mongodb_database_name') # Replace with your DB name
    evidence_collection = db.evidence
    # Assuming 'project_id' is the linking field in the MongoDB evidence documents
    evidence_list = list(evidence_collection.find({"project_id": self.id}))
    return evidence_list


class EvidenceKSBLink(Base):
    __tablename__ = "evidence_ksb_link"

    evidence_id = Column(String, primary_key=True) # Storing MongoDB _id as a string
    ksb_id = Column(Integer, ForeignKey("ksbs.id"), primary_key=True)

    ksb = relationship("KSB", back_populates="evidence_links")
    # Need to define relationship to evidence from MongoDB separately
    # project = relationship("Project", back_populates="evidence") # This relationship needs adjustment

class LearningLog(Base):
    __tablename__ = "learning_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime)
    duration_minutes = Column(Integer)
    description = Column(Text)
    evidence_id = Column(String, nullable=True) # Storing MongoDB _id as a string

    user = relationship("User", back_populates="learning_logs")
    # Need to define relationship to evidence from MongoDB separately