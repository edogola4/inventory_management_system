# schemas/transaction.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from models.transaction import TransactionType

class TransactionItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class TransactionItemCreate(TransactionItemBase):
    pass

class TransactionItem(TransactionItemBase):
    id: int
    transaction_id: int
    
    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    transaction_type: TransactionType
    reference_number: str
    notes: Optional[str] = None
    supplier_id: Optional[int] = None

class TransactionCreate(TransactionBase):
    items: List[TransactionItemCreate]

class Transaction(TransactionBase):
    id: int
    date: datetime
    items: List[TransactionItem] = []
    
    class Config:
        orm_mode = True