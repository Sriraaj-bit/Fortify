from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class BudgetBase(BaseModel):
    category: str
    limit_amount: float = Field(..., gt=0)
    period_start: datetime
    period_end: datetime


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category: Optional[str] = None
    limit_amount: Optional[float] = Field(None, gt=0)
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None


class BudgetInDBBase(BudgetBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class BudgetInDB(BudgetInDBBase):
    pass


class BudgetResponse(BudgetInDBBase):
    pass