from sqlalchemy.orm import Session
from app.db.models import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate
from uuid import UUID
from typing import List, Optional


def get_budget(db: Session, budget_id: UUID, user_id: UUID):
    return db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == user_id
    ).first()


def get_budgets(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return db.query(Budget).filter(
        Budget.user_id == user_id
    ).offset(skip).limit(limit).all()


def create_budget(db: Session, budget_in: BudgetCreate, user_id: UUID):
    db_budget = Budget(
        **budget_in.dict(),
        user_id=user_id
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def update_budget(db: Session, budget_id: UUID, user_id: UUID, budget_in: BudgetUpdate):
    db_budget = get_budget(db, budget_id, user_id)
    if not db_budget:
        return None
    update_data = budget_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_budget, field, value)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def delete_budget(db: Session, budget_id: UUID, user_id: UUID):
    db_budget = get_budget(db, budget_id, user_id)
    if not db_budget:
        return False
    db.delete(db_budget)
    db.commit()
    return True