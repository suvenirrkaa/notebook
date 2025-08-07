from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models.base import Base  

engine = create_engine("sqlite:///notebook.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
