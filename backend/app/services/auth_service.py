from sqlalchemy.orm import Session
from app.db.models import User, UserSession
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.schemas.user import UserCreate, UserResponse
from datetime import datetime, timedelta
import uuid


def create_user(db: Session, user_in: UserCreate):
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_verified=False  # Will be verified via email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user_session(db: Session, user_id: uuid.UUID):
    refresh_token = create_refresh_token()
    expires_at = datetime.utcnow() + timedelta(days=7)  # 7 days
    db_session = UserSession(
        user_id=user_id,
        refresh_token=refresh_token,
        expires_at=expires_at
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session, refresh_token


def verify_refresh_token(db: Session, refresh_token: str):
    db_session = db.query(UserSession).filter(UserSession.refresh_token == refresh_token).first()
    if not db_session:
        return None
    if db_session.expires_at < datetime.utcnow():
        # Token expired, delete it
        db.delete(db_session)
        db.commit()
        return None
    return db_session.user


def create_access_token_for_user(db: Session, user: User):
    access_token_expires = timedelta(minutes=30)  # Could be from settings
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return access_token