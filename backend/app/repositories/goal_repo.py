from sqlalchemy.orm import Session
from app.db.models import Goal
from app.schemas.goal import GoalCreate, GoalUpdate
from uuid import UUID
from typing import List, Optional


def get_goal(db: Session, goal_id: UUID, user_id: UUID):
    return db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == user_id
    ).first()


def get_goals(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return db.query(Goal).filter(
        Goal.user_id == user_id
    ).offset(skip).limit(limit).all()


def create_goal(db: Session, goal_in: GoalCreate, user_id: UUID):
    db_goal = Goal(
        **goal_in.dict(),
        user_id=user_id
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def update_goal(db: Session, goal_id: UUID, user_id: UUID, goal_in: GoalUpdate):
    db_goal = get_goal(db, goal_id, user_id)
    if not db_goal:
        return None
    update_data = goal_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_goal, field, value)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def delete_goal(db: Session, goal_id: UUID, user_id: UUID):
    db_goal = get_goal(db, goal_id, user_id)
    if not db_goal:
        return False
    db.delete(db_goal)
    db.commit()
    return Truev