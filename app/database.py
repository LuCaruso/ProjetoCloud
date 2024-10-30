from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os

DATABASE_USER=os.getenv("DATABASE_USER")
DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD")
DATABASE_NAME=os.getenv("DATABASE_NAME")
DATABASE_HOST=os.getenv("DATABASE_HOST")

db = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost:5432/{DATABASE_NAME}"

SQLALCHEMY_DATABASE_URL = db

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
