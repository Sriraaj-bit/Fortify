from sqlalchemy.orm import Session
from app.repositories.goal_repo import (
    get_goal,
    get_goals,
    create_goal,
    update_goal,
    delete_goal
)
from app.schemas.goal import GoalCreate, GoalUpdate
from uuid import UUID
from typing import List


def get_user_goals(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return get_goals(db, user_id=user_id, skip=skip, limit=limit)


def get_user_goal(db: Session, goal_id: UUID, user_id: UUID):
    return get_goal(db, goal_id=goal_id, user_id=user_id)


def create_user_goal(db: Session, goal_in: GoalCreate, user_id: UUID):
    return create_goal(db, goal_in=goal_in, user_id=user_id)


def update_user_goal(db: Session, goal_id: UUID, user_id: UUID, goal_in: GoalUpdate):
    return update_goal(db, goal_id=goal_id, user_id=user_id, goal_in=goal_in)


def delete_user_goal(db: Session, goal_id: UUID, user_id: UUID):
    return delete_goal(db, goal_id=goal_id, user_id=user_id)