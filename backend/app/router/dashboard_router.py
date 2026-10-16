from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.dashboard import DashboardResponse, DashboardSummary
from app.services.dashboard_service import get_dashboard_summary, get_recent_transactions, get_budget_progress, get_goal_progress
from app.utils.dependencies import get_current_user
from app.db.models import User
from uuid import UUID
from typing import List

router = APIRouter()

@router.get("/", response_model=DashboardResponse)
def read_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    summary = get_dashboard_summary(db, user_id=current_user.id)
    recent_transactions = get_recent_transactions(db, user_id=current_user.id)
    budget_progress = get_budget_progress(db, user_id=current_user.id)
    goal_progress = get_goal_progress(db, user_id=current_user.id)

    return {
        "summary": summary,
        "recent_transactions": recent_transactions,
        "budget_progress": budget_progress,
        "goal_progress": goal_progress
    }