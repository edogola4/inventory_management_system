# schemas/supplier.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class SupplierBase(BaseModel):
    name: str
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(SupplierBase):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class Supplier(SupplierBase):
    id: int
    
    class Config:
        orm_mode = True

class SupplierWithProducts(Supplier):
    products: List["ProductBase"] = [] # type: ignore
    
    class Config:
        orm_mode = True
