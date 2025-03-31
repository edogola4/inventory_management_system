# init_db.py
from models.base import Base
from config import engine  # assuming your engine is defined in config.py

# Import your model classes so that they're registered with the Base metadata
from models.category import Category
from models.product import Product

# Create all tables
Base.metadata.create_all(engine)
print("Database tables created.")
