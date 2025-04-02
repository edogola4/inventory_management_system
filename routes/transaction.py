# routes/transaction.py 
from flask import Blueprint, request, jsonify, abort, make_response
from models.base import get_db
from controllers import transaction as transaction_controller
from models.transaction import TransactionType
from models.product import Product

# Change the URL prefix to avoid conflict with the web routes
router = Blueprint('transaction_api', __name__, url_prefix='/api/transactions')

@router.route('/', methods=['POST'])
def create_transaction():
    transaction_data = request.get_json()
    db = next(get_db())
    try:
        transaction = transaction_controller.create_transaction(db, transaction_data)
        return jsonify(transaction.to_dict()), 201
    except ValueError as e:
        return make_response(jsonify({"detail": str(e)}), 400)

@router.route('/', methods=['GET'])
def read_transactions():
    skip = request.args.get('skip', default=0, type=int)
    limit = request.args.get('limit', default=100, type=int)
    db = next(get_db())
    transactions = transaction_controller.get_transactions(db, skip=skip, limit=limit)
    transactions_data = [t.to_dict() for t in transactions]
    return jsonify(transactions_data)

@router.route('/<int:transaction_id>', methods=['GET'])
def read_transaction(transaction_id):
    db = next(get_db())
    transaction = transaction_controller.get_transaction(db, transaction_id)
    if transaction is None:
        abort(404, description="Transaction not found")
    return jsonify(transaction.to_dict())

@router.route('/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    db = next(get_db())
    try:
        success = transaction_controller.delete_transaction(db, transaction_id)
        if not success:
            abort(404, description="Transaction not found")
        return '', 204
    except ValueError as e:
        abort(400, description=str(e))