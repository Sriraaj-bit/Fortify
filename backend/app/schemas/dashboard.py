from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class DashboardSummary(BaseModel):
    total_balance: float
    total_income: float
    total_expenses: float
    savings: float
    monthly_income: float
    monthly_expenses: float
    monthly_savings: float


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    recent_transactions: List[dict]  # We'll use dict for simplicity, could be TransactionResponse
    budget_progress: List[dict]
    goal_progress: List[dict]