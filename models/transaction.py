# models/transaction.py
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from models.base import Base

class TransactionType(enum.Enum):
    PURCHASE = "purchase"
    SALE = "sale"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    reference_number = Column(String(50), unique=True)
    notes = Column(String(500))
    
    # Relationships
    transaction_items = relationship("TransactionItem", back_populates="transaction", cascade="all, delete-orphan")
    
    # Supplier relationship
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    supplier = relationship("Supplier", back_populates="transactions")
    
    # Many-to-many relationship to products (viewonly)
    products = relationship(
        "Product",
        secondary="transaction_items",
        primaryjoin="Transaction.id == TransactionItem.transaction_id",
        secondaryjoin="TransactionItem.product_id == Product.id",
        viewonly=True
    )
    
    def __repr__(self):
        return f"<Transaction id={self.id}, type={self.transaction_type.value}, date={self.date}>"
    
    def to_dict(self):
        """Convert a Transaction instance to a dict."""
        return {
            "id": self.id,
            "transaction_type": self.transaction_type.value if self.transaction_type else None,
            "date": self.date.isoformat() if self.date else None,
            "reference_number": self.reference_number,
            "notes": self.notes,
            "supplier_id": self.supplier_id,
            "transaction_items": [item.to_dict() for item in self.transaction_items],
        }

class TransactionItem(Base):
    __tablename__ = "transaction_items"
    
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    
    # Relationships
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    transaction = relationship("Transaction", back_populates="transaction_items")
    
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product", back_populates="transaction_items")
    
    def __repr__(self):
        return f"<TransactionItem id={self.id}, product_id={self.product_id}, quantity={self.quantity}>"
    
    @property
    def total_price(self):
        """Calculate the total price for this transaction item."""
        return self.quantity * self.unit_price
    
    def to_dict(self):
        """Convert a TransactionItem instance to a dict."""
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
        }
