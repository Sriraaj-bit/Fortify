from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum as PyEnum


class TransactionType(str, PyEnum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: TransactionType
    category: Optional[str] = None
    description: Optional[str] = None
    date: datetime
    currency: str = "USD"
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    currency: Optional[str] = None
    notes: Optional[str] = None


class TransactionInDBBase(TransactionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class TransactionInDB(TransactionInDBBase):
    pass


class TransactionResponse(TransactionInDBBase):
    pass