# controllers/transaction.py
from sqlalchemy.orm import Session
from models.transaction import Transaction, TransactionItem, TransactionType
from models.product import Product  # Ensure your Product model is defined accordingly

def create_transaction(db: Session, transaction_data: dict):
    """Create a new transaction with its items."""
    # Create a new Transaction instance
    db_transaction = Transaction(
        transaction_type=transaction_data.get("transaction_type"),
        reference_number=transaction_data.get("reference_number"),
        notes=transaction_data.get("notes"),
        supplier_id=transaction_data.get("supplier_id")
    )
    db.add(db_transaction)
    db.flush()  # Flush to generate an ID
    
    # Create transaction items and update product quantity
    for item_data in transaction_data.get("items", []):
        db_item = TransactionItem(
            transaction_id=db_transaction.id,
            product_id=item_data.get("product_id"),
            quantity=item_data.get("quantity"),
            unit_price=item_data.get("unit_price")
        )
        db.add(db_item)
        
        # Update product quantity based on transaction type
        product = db.query(Product).filter(Product.id == item_data.get("product_id")).first()
        if transaction_data.get("transaction_type") == TransactionType.PURCHASE:
            product.quantity += item_data.get("quantity")
        elif transaction_data.get("transaction_type") == TransactionType.SALE:
            if product.quantity >= item_data.get("quantity"):
                product.quantity -= item_data.get("quantity")
            else:
                db.rollback()
                raise ValueError(f"Insufficient quantity for product: {product.name}")
    
    db.commit()
    return db_transaction

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    """Get all transactions."""
    return db.query(Transaction).offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int):
    """Get a specific transaction by ID."""
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def delete_transaction(db: Session, transaction_id: int):
    """Delete a transaction by ID and revert product quantity changes."""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        for item in transaction.transaction_items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if transaction.transaction_type == TransactionType.PURCHASE:
                if product.quantity >= item.quantity:
                    product.quantity -= item.quantity
                else:
                    raise ValueError(f"Cannot delete transaction: would result in negative inventory for {product.name}")
            elif transaction.transaction_type == TransactionType.SALE:
                product.quantity += item.quantity
        
        db.delete(transaction)
        db.commit()
        return True
    return False
