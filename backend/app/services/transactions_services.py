from sqlalchemy.orm import Session
from app.repositories.transaction_repo import (
    get_transaction,
    get_transactions,
    create_transaction,
    update_transaction,
    delete_transaction
)
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from uuid import UUID
from typing import List


def get_user_transactions(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return get_transactions(db, user_id=user_id, skip=skip, limit=limit)


def get_user_transaction(db: Session, transaction_id: UUID, user_id: UUID):
    return get_transaction(db, transaction_id=transaction_id, user_id=user_id)


def create_user_transaction(db: Session, transaction_in: TransactionCreate, user_id: UUID):
    return create_transaction(db, transaction_in=transaction_in, user_id=user_id)


def update_user_transaction(db: Session, transaction_id: UUID, user_id: UUID, transaction_in: TransactionUpdate):
    return update_transaction(db, transaction_id=transaction_id, user_id=user_id, transaction_in=transaction_in)


def delete_user_transaction(db: Session, transaction_id: UUID, user_id: UUID):
    return delete_transaction(db, transaction_id=transaction_id, user_id=user_id)