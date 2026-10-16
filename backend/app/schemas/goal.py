from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class GoalBase(BaseModel):
    target_amount: float = Field(..., gt=0)
    current_amount: float = Field(0, ge=0)
    target_date: Optional[datetime] = None
    description: Optional[str] = None


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    target_amount: Optional[float] = Field(None, gt=0)
    current_amount: Optional[float] = Field(None, ge=0)
    target_date: Optional[datetime] = None
    description: Optional[str] = None


class GoalInDBBase(GoalBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class GoalInDB(GoalInDBBase):
    pass


class GoalResponse(GoalInDBBase):
    pass