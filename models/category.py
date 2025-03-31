from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.exc import SQLAlchemyError
from models.base import Base, Session

class Category(Base):
    """Category model representing product categories."""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    _name = Column("name", String(50), nullable=False, unique=True)
    _description = Column("description", String(255))
    
    # Relationship with Product
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str) or len(value.strip()) < 2:
            raise ValueError("Category name must be a string with at least 2 characters")
        self._name = value.strip()
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if value and not isinstance(value, str):
            raise ValueError("Description must be a string")
        self._description = value.strip() if value else value
    
    @classmethod
    def create(cls, name, description=""):
        """Create a new category."""
        session = Session()
        try:
            # Create a blank instance, then set properties so that setters are used.
            category = cls()
            category.name = name
            category.description = description
            session.add(category)
            session.commit()
            return category
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_all(cls):
        """Get all categories with their products eagerly loaded."""
        session = Session()
        try:
            categories = session.query(cls).options(joinedload(cls.products)).all()
            return categories
        finally:
            session.close()
    
    @classmethod
    def find_by_id(cls, id):
        """Find a category by ID with its products eagerly loaded."""
        session = Session()
        try:
            category = session.query(cls)\
                .options(joinedload(cls.products))\
                .filter_by(id=id)\
                .first()
            return category
        finally:
            session.close()
    
    @classmethod
    def find_by_name(cls, name):
        """Find a category by name."""
        session = Session()
        try:
            category = session.query(cls).filter(cls._name == name).first()
            return category
        finally:
            session.close()
    
    def update(self, name=None, description=None):
        """Update the category."""
        session = Session()
        try:
            if name:
                self.name = name
            if description is not None:
                self.description = description
            session.add(self)
            session.commit()
            return self
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self):
        """Delete the category."""
        session = Session()
        try:
            session.delete(self)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def __repr__(self):
        return f"<Category id={self.id}, name={self.name}>"
