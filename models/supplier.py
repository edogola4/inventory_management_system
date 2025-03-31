from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

# Association table for many-to-many between Products and Suppliers
product_supplier_association = Table(
    'product_supplier', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('supplier_id', Integer, ForeignKey('suppliers.id'))
)

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    contact_info = Column(String(255))
    
    # Many-to-many with Products
    products = relationship("Product", secondary=product_supplier_association, back_populates="suppliers")
    
    # One-to-many: a supplier can have many transactions (for purchases)
    transactions = relationship("Transaction", back_populates="supplier")
    
    def __repr__(self):
        return f"<Supplier id={self.id}, name={self.name}>"
