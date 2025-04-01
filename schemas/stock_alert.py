# schemas/stock_alert.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SupplierInfo(BaseModel):
    id: int
    name: str

class StockAlert(BaseModel):
    product_id: int
    product_name: str
    current_quantity: int
    reorder_level: int
    recommended_quantity: int
    suppliers: List[SupplierInfo] = []