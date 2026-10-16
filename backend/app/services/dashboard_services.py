from sqlalchemy.orm import Session
from app.db.models import Transaction, Budget, Goal
from app.schemas.transaction import TransactionResponse
from app.schemas.budget import BudgetResponse
from app.schemas.goal import GoalResponse
from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy import func, and_
from datetime import datetime, timedelta


def get_dashboard_summary(db: Session, user_id: UUID):
    # Get current date for monthly calculations
    now = datetime.utcnow()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Calculate total balance (income - expenses)
    total_income = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "income"
    ).scalar() or 0

    total_expenses = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense"
    ).scalar() or 0

    total_balance = float(total_income) - float(total_expenses)
    savings = float(total_income) - float(total_expenses)  # Same as balance for now

    # Calculate monthly totals
    monthly_income = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "income",
        Transaction.date >= start_of_month
    ).scalar() or 0

    monthly_expenses = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense",
        Transaction.date >= start_of_month
    ).scalar() or 0

    monthly_savings = float(monthly_income) - float(monthly_expenses)

    return {
        "total_balance": float(total_balance),
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "savings": float(savings),
        "monthly_income": float(monthly_income),
        "monthly_expenses": float(monthly_expenses),
        "monthly_savings": float(monthly_savings)
    }


def get_recent_transactions(db: Session, user_id: UUID, limit: int = 5):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(Transaction.date.desc()).limit(limit).all()

    # Convert to dict for simplicity
    return [
        {
            "id": str(t.id),
            "amount": float(t.amount),
            "type": t.type.value if hasattr(t.type, 'value') else str(t.type),
            "category": t.category,
            "description": t.description,
            "date": t.date.isoformat() if t.date else None,
            "currency": t.currency
        }
        for t in transactions
    ]


def get_budget_progress(db: Session, user_id: UUID):
    # Get current date
    now = datetime.utcnow()

    # Get active budgets (where now is between period_start and period_end)
    budgets = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.period_start <= now,
        Budget.period_end >= now
    ).all()

    progress = []
    for budget in budgets:
        # Calculate spent amount for this budget category in the period
        spent = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.user_id == user_id,
            Transaction.category == budget.category,
            Transaction.type == "expense",  # Assuming budgets are for expenses
            Transaction.date >= budget.period_start,
            Transaction.date <= budget.period_end
        ).scalar() or 0

        spent_float = float(spent)
        limit_float = float(budget.limit_amount)
        percentage = min((spent_float / limit_float) * 100, 100) if limit_float > 0 else 0

        progress.append({
            "id": str(budget.id),
            "category": budget.category,
            "limit_amount": limit_float,
            "spent_amount": spent_float,
            "remaining_amount": max(limit_float - spent_float, 0),
            "percentage_used": percentage
        })

    return progress


def get_goal_progress(db: Session, user_id: UUID):
    goals = db.query(Goal).filter(Goal.user_id == user_id).all()

    progress = []
    for goal in goals:
        target_float = float(goal.target_amount)
        current_float = float(goal.current_amount)
        percentage = min((current_float / target_float) * 100, 100) if target_float > 0 else 0

        progress.append({
            "id": str(goal.id),
            "target_amount": target_float,
            "current_amount": current_float,
            "remaining_amount": max(target_float - current_float, 0),
            "percentage_complete": percentage,
            "target_date": goal.target_date.isoformat() if goal.target_date else None,
            "description": goal.description
        })

    return progress