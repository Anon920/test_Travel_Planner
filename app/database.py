from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE = 'sqlite:///./travel_planner.db'

engine = create_engine(DATABASE, connect_args={"check_same_thread": False})

LocalSession = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
