from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
import datetime

from models.base import Base, Session

class Product(Base):
    """Product model representing inventory items."""
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationship with Category
    category = relationship("Category", back_populates="products")
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str) or len(value) < 2:
            raise ValueError("Product name must be a string with at least 2 characters")
        self._name = value
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        try:
            value = float(value)
            if value < 0:
                raise ValueError("Price cannot be negative")
            self._price = value
        except (ValueError, TypeError):
            raise ValueError("Price must be a positive number")
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        try:
            value = int(value)
            if value < 0:
                raise ValueError("Quantity cannot be negative")
            self._quantity = value
        except (ValueError, TypeError):
            raise ValueError("Quantity must be a positive integer")
    
    @classmethod
    def create(cls, name, price, category_id, description="", quantity=0):
        """Create a new product."""
        session = Session()
        try:
            product = cls(
                name=name,
                price=price,
                category_id=category_id,
                description=description,
                quantity=quantity
            )
            session.add(product)
            session.commit()
            return product
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_all(cls):
        """Get all products."""
        session = Session()
        try:
            products = session.query(cls).all()
            return products
        finally:
            session.close()
    
    @classmethod
    def find_by_id(cls, id):
        """Find a product by ID."""
        session = Session()
        try:
            product = session.query(cls).filter_by(id=id).first()
            return product
        finally:
            session.close()
    
    @classmethod
    def find_by_category(cls, category_id):
        """Find products by category ID."""
        session = Session()
        try:
            products = session.query(cls).filter_by(category_id=category_id).all()
            return products
        finally:
            session.close()
    
    def update(self, name=None, price=None, description=None, quantity=None, category_id=None):
        """Update the product."""
        session = Session()
        try:
            if name:
                self.name = name
            if price is not None:
                self.price = price
            if description is not None:
                self.description = description
            if quantity is not None:
                self.quantity = quantity
            if category_id:
                self.category_id = category_id
            
            self.updated_at = datetime.datetime.utcnow()
            session.add(self)
            session.commit()
            return self
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self):
        """Delete the product."""
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
        return f"<Product id={self.id}, name={self.name}, quantity={self.quantity}>"