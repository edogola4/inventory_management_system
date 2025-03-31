from models.base import Base
from config import engine  # Ensure your engine is configured correctly

# Import your model classes so that they're registered with the Base metadata
from models.category import Category
from models.product import Product

def init_db():
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")

if __name__ == '__main__':
    init_db()
