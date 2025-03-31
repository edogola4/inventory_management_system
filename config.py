import os
from pathlib import Path
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URI = f"sqlite:///{BASE_DIR}/inventory.db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI, echo=True)