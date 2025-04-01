# services/transaction_service.py
from models.transaction import Transaction, TransactionItem, TransactionType
from models.product import Product
from sqlalchemy.orm import Session

class TransactionService:
    def __init__(self, session: Session):
        self.session = session
        
    def create_transaction(self, transaction_type, product_id, quantity, price_per_unit, 
                             reference_number=None, notes=None):
        """Create a new transaction with a transaction item and update product quantity."""
        # Validate product exists
        product = self.session.query(Product).get(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} does not exist")
            
        # Create transaction without passing product-related fields
        transaction = Transaction(
            transaction_type=transaction_type,
            reference_number=reference_number,
            notes=notes
        )
        self.session.add(transaction)
        self.session.flush()  # Flush to generate transaction.id
        
        # Create a transaction item with product details
        transaction_item = TransactionItem(
            transaction_id=transaction.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=price_per_unit
        )
        self.session.add(transaction_item)
        
        # Update product quantity based on transaction type
        if transaction_type == TransactionType.PURCHASE:
            product.quantity += quantity
        elif transaction_type == TransactionType.SALE:
            if product.quantity < quantity:
                raise ValueError(f"Insufficient stock. Available: {product.quantity}, Requested: {quantity}")
            product.quantity -= quantity
            
        self.session.commit()
        return transaction
        
    def get_transaction(self, transaction_id):
        """Get transaction by ID."""
        return self.session.query(Transaction).get(transaction_id)
        
    def get_all_transactions(self):
        """Get all transactions."""
        return self.session.query(Transaction).all()
        
    def get_transactions_by_product(self, product_id):
        """Get all transactions for a specific product by joining TransactionItem."""
        return (
            self.session.query(Transaction)
            .join(TransactionItem)
            .filter(TransactionItem.product_id == product_id)
            .all()
        )
        
    def get_transactions_by_type(self, transaction_type):
        """Get all transactions of a specific type."""
        return self.session.query(Transaction).filter(Transaction.transaction_type == transaction_type).all()
        
    def delete_transaction(self, transaction_id):
        """Delete a transaction and revert product quantity changes."""
        transaction = self.get_transaction(transaction_id)
        if not transaction:
            raise ValueError(f"Transaction with ID {transaction_id} does not exist")
        
        # Revert product quantity change for each transaction item
        for item in transaction.transaction_items:
            product = self.session.query(Product).get(item.product_id)
            if transaction.transaction_type == TransactionType.PURCHASE:
                if product.quantity < item.quantity:
                    raise ValueError("Cannot delete transaction; product quantity would become negative.")
                product.quantity -= item.quantity
            elif transaction.transaction_type == TransactionType.SALE:
                product.quantity += item.quantity
            
        self.session.delete(transaction)
        self.session.commit()
        return True
