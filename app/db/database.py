# This file sets uup connection to SQLite database and creates a session factory for interacting with it.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./notes.db"

engine = create_engine(DATABASE_URL, echo=True)
# create engine to establish a connection with a local SQLite database
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# SessionLocal is the session factory to perfom DB operations

Base = declarative_base() # Is the class where all the models inherit from

# get_db() is a dependency used with FastAPIs Depends() , it gives a session to routes and ensure its properly closed after use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        