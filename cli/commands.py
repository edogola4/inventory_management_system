from services.transaction_service import TransactionService
from services.product_service import ProductService
from models.transaction import TransactionType
from .helpers import print_success, print_error, print_warning, print_info, print_title, print_table, get_input, validate_positive_integer, validate_positive_number

# cli/commands.py (add these functions to your existing CLI commands)
from models.transaction import TransactionType
from services.transaction_service import TransactionService
from services.product_service import ProductService
from .helpers import (
    print_title, print_table, print_success, print_error, print_info, print_warning,
    confirm_action, get_input, validate_required_string, validate_positive_number,
    validate_positive_integer
)

def list_transactions(session):
    """List all transactions."""
    service = TransactionService(session)
    transactions = service.get_all_transactions()
    
    if not transactions:
        print("No transactions found.")
        return
        
    print("\n--- TRANSACTIONS ---")
    print(f"{'ID':<4} {'TYPE':<10} {'PRODUCT':<20} {'QTY':<6} {'PRICE':<10} {'TOTAL':<10} {'DATE':<16} {'REFERENCE':<15}")
    print("-" * 90)
    
    for t in transactions:
        print(f"{t.id:<4} {t.transaction_type.name:<10} {t.product.name[:18]:<20} {t.quantity:<6} ${t.price_per_unit:<8.2f} ${t.total_amount:<8.2f} {t.transaction_date.strftime('%Y-%m-%d %H:%M'):<16} {(t.reference_number or '')[:14]:<15}")
    print()

def add_transaction(session):
    """Add a new transaction."""
    product_service = ProductService(session)
    transaction_service = TransactionService(session)
    
    # List available products
    products = product_service.get_all_products()
    if not products:
        print("No products available. Please add products first.")
        return
        
    print("\n--- Available Products ---")
    for p in products:
        print(f"{p.id}: {p.name} (Stock: {p.quantity})")
    
    # Get transaction details
    try:
        product_id = int(input("\nProduct ID: "))
        product = product_service.get_product(product_id)
        if not product:
            print(f"Product with ID {product_id} does not exist.")
            return
            
        print("\nTransaction Types:")
        print("1. Purchase (adds to inventory)")
        print("2. Sale (removes from inventory)")
        
        choice = int(input("Choose transaction type (1-2): "))
        if choice == 1:
            transaction_type = TransactionType.PURCHASE
        elif choice == 2:
            transaction_type = TransactionType.SALE
        else:
            print("Invalid choice.")
            return
            
        quantity = int(input("Quantity: "))
        price_per_unit = float(input("Price per unit ($): "))
        reference_number = input("Reference number (optional): ").strip() or None
        notes = input("Notes (optional): ").strip() or None
        
        transaction = transaction_service.create_transaction(
            transaction_type=transaction_type,
            product_id=product_id,
            quantity=quantity,
            price_per_unit=price_per_unit,
            reference_number=reference_number,
            notes=notes
        )
        
        print(f"\nTransaction created successfully! ID: {transaction.id}")
    except ValueError as e:
        print(f"Error: {str(e)}")

def delete_transaction(session):
    """Delete a transaction."""
    service = TransactionService(session)
    
    try:
        transaction_id = int(input("Enter transaction ID to delete: "))
        service.delete_transaction(transaction_id)
        print(f"Transaction {transaction_id} deleted successfully!")
    except ValueError as e:
        print(f"Error: {str(e)}")
