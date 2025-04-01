# controllers/supplier.py
from sqlalchemy.orm import Session
from models.supplier import Supplier
from schemas.supplier import SupplierCreate, SupplierUpdate
from typing import List, Optional

def create_supplier(db: Session, supplier_data: SupplierCreate):
    """Create a new supplier"""
    db_supplier = Supplier(
        name=supplier_data.name,
        contact_name=supplier_data.contact_name,
        email=supplier_data.email,
        phone=supplier_data.phone,
        address=supplier_data.address
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def get_suppliers(db: Session, skip: int = 0, limit: int = 100):
    """Get all suppliers"""
    return db.query(Supplier).offset(skip).limit(limit).all()

def get_supplier(db: Session, supplier_id: int):
    """Get a specific supplier by ID"""
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def update_supplier(db: Session, supplier_id: int, supplier_data: SupplierUpdate):
    """Update a supplier"""
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if db_supplier:
        for key, value in supplier_data.dict(exclude_unset=True).items():
            setattr(db_supplier, key, value)
        db.commit()
        db.refresh(db_supplier)
    return db_supplier

def delete_supplier(db: Session, supplier_id: int):
    """Delete a supplier"""
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if db_supplier:
        db.delete(db_supplier)
        db.commit()
        return True
    return False

def link_supplier_product(db: Session, supplier_id: int, product_id: int):
    """Link a supplier to a product"""
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return None
    
    from models.product import Product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    
    supplier.products.append(product)
    db.commit()
    return supplier

def unlink_supplier_product(db: Session, supplier_id: int, product_id: int):
    """Unlink a supplier from a product"""
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return None
    
    from models.product import Product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    
    supplier.products.remove(product)
    db.commit()
    return supplier