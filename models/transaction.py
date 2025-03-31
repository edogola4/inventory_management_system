from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from models.base import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=True)  # Optional for sales
    transaction_type = Column(String(50), nullable=False)  # "purchase" or "sale"
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="transactions")
    supplier = relationship("Supplier", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction id={self.id}, type={self.transaction_type}, quantity={self.quantity}, total={self.total_amount}>"
