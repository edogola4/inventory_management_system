# routes/supplier.py
"""from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.base import get_db
from controllers import supplier as supplier_controller
from schemas.supplier import Supplier, SupplierCreate, SupplierUpdate

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.post("/", response_model=Supplier, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier_data: SupplierCreate, db: Session = Depends(get_db)):
    return supplier_controller.create_supplier(db, supplier_data)

@router.get("/", response_model=List[Supplier])
def read_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return supplier_controller.get_suppliers(db, skip=skip, limit=limit)

@router.get("/{supplier_id}", response_model=Supplier)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = supplier_controller.get_supplier(db, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.put("/{supplier_id}", response_model=Supplier)
def update_supplier(
    supplier_id: int, supplier_data: SupplierUpdate, db: Session = Depends(get_db)
):
    supplier = supplier_controller.update_supplier(db, supplier_id, supplier_data)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    result = supplier_controller.delete_supplier(db, supplier_id)
    if not result:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"detail": "Supplier deleted successfully"}

@router.post("/{supplier_id}/products/{product_id}")
def link_supplier_to_product(
    supplier_id: int, product_id: int, db: Session = Depends(get_db)
):
    result = supplier_controller.link_supplier_product(db, supplier_id, product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Supplier or product not found")
    return {"detail": "Supplier linked to product successfully"}

@router.delete("/{supplier_id}/products/{product_id}")
def unlink_supplier_from_product(
    supplier_id: int, product_id: int, db: Session = Depends(get_db)
):
    result = supplier_controller.unlink_supplier_product(db, supplier_id, product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Supplier or product not found")
    return {"detail": "Supplier unlinked from product successfully"}
"""
from flask import Blueprint, request, jsonify, abort, make_response
from sqlalchemy.orm import Session
from models.base import get_db  # Assumes get_db is a generator that yields a DB session
from controllers import supplier as supplier_controller

router = Blueprint("supplier", __name__, url_prefix="/suppliers")

@router.route("/", methods=["POST"])
def create_supplier():
    # Get JSON payload from the request
    supplier_data = request.get_json()
    db = next(get_db())
    try:
        result = supplier_controller.create_supplier(db, supplier_data)
        # Return the created supplier as JSON with a 201 status code
        return jsonify(result), 201
    except Exception as e:
        # If an error occurs, return a 400 error with the error message
        return make_response(jsonify({"detail": str(e)}), 400)

@router.route("/", methods=["GET"])
def read_suppliers():
    # Retrieve query parameters for pagination
    skip = request.args.get("skip", default=0, type=int)
    limit = request.args.get("limit", default=100, type=int)
    db = next(get_db())
    result = supplier_controller.get_suppliers(db, skip=skip, limit=limit)
    return jsonify(result)

@router.route("/<int:supplier_id>", methods=["GET"])
def read_supplier(supplier_id):
    db = next(get_db())
    result = supplier_controller.get_supplier(db, supplier_id)
    if result is None:
        abort(404, description="Supplier not found")
    return jsonify(result)

@router.route("/<int:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id):
    supplier_data = request.get_json()
    db = next(get_db())
    result = supplier_controller.update_supplier(db, supplier_id, supplier_data)
    if result is None:
        abort(404, description="Supplier not found")
    return jsonify(result)

@router.route("/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id):
    db = next(get_db())
    result = supplier_controller.delete_supplier(db, supplier_id)
    if not result:
        abort(404, description="Supplier not found")
    # A 204 status code normally implies no content, but you can return a message if desired
    return jsonify({"detail": "Supplier deleted successfully"}), 204

@router.route("/<int:supplier_id>/products/<int:product_id>", methods=["POST"])
def link_supplier_to_product(supplier_id, product_id):
    db = next(get_db())
    result = supplier_controller.link_supplier_product(db, supplier_id, product_id)
    if result is None:
        abort(404, description="Supplier or product not found")
    return jsonify({"detail": "Supplier linked to product successfully"})

@router.route("/<int:supplier_id>/products/<int:product_id>", methods=["DELETE"])
def unlink_supplier_from_product(supplier_id, product_id):
    db = next(get_db())
    result = supplier_controller.unlink_supplier_product(db, supplier_id, product_id)
    if result is None:
        abort(404, description="Supplier or product not found")
    return jsonify({"detail": "Supplier unlinked from product successfully"})
