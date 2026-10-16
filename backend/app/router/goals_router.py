from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from app.services.goal_service import (
    get_user_goals,
    get_user_goal,
    create_user_goal,
    update_user_goal,
    delete_user_goal
)
from app.utils.dependencies import get_current_user
from app.db.models import User
from uuid import UUID
from typing import List

router = APIRouter()

@router.get("/", response_model=List[GoalResponse])
def read_goals(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    goals = get_user_goals(db, user_id=current_user.id, skip=skip, limit=limit)
    return goals

@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
    goal_in: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_user_goal(db, goal_in=goal_in, user_id=current_user.id)

@router.get("/{goal_id}", response_model=GoalResponse)
def read_goal(
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    goal = get_user_goal(db, goal_id=goal_id, user_id=current_user.id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@router.patch("/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: UUID,
    goal_in: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    goal = update_user_goal(db, goal_id=goal_id, user_id=current_user.id, goal_in=goal_in)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = delete_user_goal(db, goal_id=goal_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
    return None