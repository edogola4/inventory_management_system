# services/stock_alerts.py
from sqlalchemy.orm import Session
from models.product import Product
from typing import List
import logging

logger = logging.getLogger(__name__)

def check_low_stock(db: Session) -> List[Product]:
    """Check for products that are below their reorder level"""
    low_stock_products = db.query(Product).filter(
        Product.quantity <= Product.reorder_level
    ).all()
    
    return low_stock_products

def generate_purchase_recommendations(db: Session) -> dict:
    """Generate purchase recommendations for low stock items"""
    low_stock_products = check_low_stock(db)
    recommendations = {}
    
    for product in low_stock_products:
        quantity_to_order = product.reorder_quantity
        recommendations[product.id] = {
            "product_id": product.id,
            "product_name": product.name,
            "current_quantity": product.quantity,
            "reorder_level": product.reorder_level,
            "recommended_quantity": quantity_to_order,
            "suppliers": [{"id": s.id, "name": s.name} for s in product.suppliers]
        }
    
    return recommendations

def log_stock_alerts(db: Session):
    """Log stock alerts to the application log"""
    low_stock_products = check_low_stock(db)
    
    if low_stock_products:
        logger.warning(f"Found {len(low_stock_products)} products below reorder level:")
        for product in low_stock_products:
            logger.warning(f"  - {product.name}: {product.quantity} units (Reorder level: {product.reorder_level})")
    else:
        logger.info("No products below reorder level.")
    
    return low_stock_products