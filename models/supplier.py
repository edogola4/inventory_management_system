# models/supplier.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base import Base

# Many-to-many relationship between suppliers and products
supplier_product = Table(
    'supplier_product',
    Base.metadata,
    Column('supplier_id', Integer, ForeignKey('suppliers.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    products = relationship("Product", secondary=supplier_product, back_populates="suppliers")
    transactions = relationship("Transaction", back_populates="supplier")

    SessionLocal = None