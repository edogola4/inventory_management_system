from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DATABASE_URI

engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))

def init_db():
    """Initialize the database tables."""
    Base.metadata.create_all(engine)



# Set expire_on_commit=False so that instances remain loaded after commit.
Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()
