from sqlalchemy.orm import Session
from app.repositories.budget_repo import (
    get_budget,
    get_budgets,
    create_budget,
    update_budget,
    delete_budget
)
from app.schemas.budget import BudgetCreate, BudgetUpdate
from uuid import UUID
from typing import List


def get_user_budgets(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return get_budgets(db, user_id=user_id, skip=skip, limit=limit)


def get_user_budget(db: Session, budget_id: UUID, user_id: UUID):
    return get_budget(db, budget_id=budget_id, user_id=user_id)


def create_user_budget(db: Session, budget_in: BudgetCreate, user_id: UUID):
    return create_budget(db, budget_in=budget_in, user_id=user_id)


def update_user_budget(db: Session, budget_id: UUID, user_id: UUID, budget_in: BudgetUpdate):
    return update_budget(db, budget_id=budget_id, user_id=user_id, budget_in=budget_in)


def delete_user_budget(db: Session, budget_id: UUID, user_id: UUID):
    return delete_budget(db, budget_id=budget_id, user_id=user_id)