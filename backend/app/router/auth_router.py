from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.services.auth_service import create_access_token_for_user, create_user, authenticate_user, get_user_by_email, create_user_session, verify_refresh_token
from app.utils.dependencies import get_current_user
from app.schemas.user import UserCreate, UserResponse, Token, EmailVerificationRequest, PasswordResetRequest, PasswordResetConfirm
from uuid import UUID
import uuid

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    user = create_user(db=db, user_in=user_in)
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create session and tokens
    db_session, refresh_token = create_user_session(db, user.id)
    access_token = create_access_token_for_user(db, user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    user = verify_refresh_token(db, refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new session and tokens (rotate refresh token)
    # Delete old session
    db.query(UserSession).filter(UserSession.refresh_token == refresh_token).delete()
    db.commit()

    db_session, new_refresh_token = create_user_session(db, user.id)
    access_token = create_access_token_for_user(db, user)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(request: EmailVerificationRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=request.email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email already verified"
        )

    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=request.email)
    if not user:
        # Don't reveal whether email exists for security
        return {"message": "If the email exists, you will receive a password reset link"}

    # In a real implementation, generate a token and send email
    # For now, we'll just return success message
    return {"message": "If the email exists, you will receive a password reset link"}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    # In a real implementation, verify the token and reset password
    # For now, we'll just return success message
    return {"message": "Password has been reset successfully"}