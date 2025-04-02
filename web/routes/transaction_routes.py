# web/routes/transaction_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.transaction import TransactionType
from services.transaction_service import TransactionService
from services.product_service import ProductService
from utils.db import get_session
from models.product import Product

# Change the URL prefix to be the main transactions endpoint for the web interface
transaction_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@transaction_bp.route('/')
def list_transactions():
    with get_session() as session:
        service = TransactionService(session)
        transactions = service.get_all_transactions()
        # Load all transaction items with their products for display
        for transaction in transactions:
            # Ensure transaction items and their products are loaded
            for item in transaction.transaction_items:
                product = item.product
        return render_template('transactions/list.html', transactions=transactions)

@transaction_bp.route('/new', methods=['GET', 'POST'])
def create_transaction():
    with get_session() as session:
        product_service = ProductService(session)
        products = product_service.get_all_products()
        
        if request.method == 'POST':
            try:
                transaction_service = TransactionService(session)
                transaction_type = TransactionType(request.form['transaction_type'])
                product_id = int(request.form['product_id'])
                quantity = int(request.form['quantity'])
                price_per_unit = float(request.form['price_per_unit'])
                reference_number = request.form.get('reference_number')
                notes = request.form.get('notes')
                
                transaction_service.create_transaction(
                    transaction_type=transaction_type,
                    product_id=product_id,
                    quantity=quantity,
                    price_per_unit=price_per_unit,
                    reference_number=reference_number,
                    notes=notes
                )
                flash('Transaction created successfully!', 'success')
                return redirect(url_for('transactions.list_transactions'))
            except ValueError as e:
                flash(str(e), 'danger')
        
        return render_template(
            'transactions/new.html', 
            products=products, 
            transaction_types=[t for t in TransactionType]
        )

@transaction_bp.route('/<int:transaction_id>')
def view_transaction(transaction_id):
    with get_session() as session:
        service = TransactionService(session)
        transaction = service.get_transaction(transaction_id)
        if not transaction:
            flash('Transaction not found', 'danger')
            return redirect(url_for('transactions.list_transactions'))
        return render_template('transactions/view.html', transaction=transaction)

@transaction_bp.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    with get_session() as session:
        service = TransactionService(session)
        try:
            service.delete_transaction(transaction_id)
            flash('Transaction deleted successfully!', 'success')
        except ValueError as e:
            flash(str(e), 'danger')
        return redirect(url_for('transactions.list_transactions'))