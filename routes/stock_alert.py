# routes/stock_alerts.py
"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from models.base import get_db
from services import stock_alerts
from schemas.stock_alert import StockAlert

router = APIRouter(prefix="/stock-alerts", tags=["stock-alerts"])

@router.get("/low-stock", response_model=List[Dict])
def get_low_stock_products(db: Session = Depends(get_db)):
    products = stock_alerts.check_low_stock(db)
    return [
        {
            "id": p.id,
            "name": p.name,
            "quantity": p.quantity,
            "reorder_level": p.reorder_level
        }
        for p in products
    ]

@router.get("/purchase-recommendations", response_model=Dict[str, StockAlert])
def get_purchase_recommendations(db: Session = Depends(get_db)):
    return stock_alerts.generate_purchase_recommendations(db)
"""

from flask import Blueprint, jsonify, abort
from models.base import get_db
from services import stock_alerts

router = Blueprint("stock_alerts", __name__, url_prefix="/stock-alerts")

@router.route("/low-stock", methods=["GET"])
def get_low_stock_products():
    # Get a database session from get_db generator
    db = next(get_db())
    products = stock_alerts.check_low_stock(db)
    result = [
        {
            "id": p.id,
            "name": p.name,
            "quantity": p.quantity,
            "reorder_level": p.reorder_level
        }
        for p in products
    ]
    return jsonify(result)

@router.route("/purchase-recommendations", methods=["GET"])
def get_purchase_recommendations():
    db = next(get_db())
    recommendations = stock_alerts.generate_purchase_recommendations(db)
    return jsonify(recommendations)
