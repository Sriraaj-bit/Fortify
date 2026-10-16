from sqlalchemy.orm import Session
from app.db.models import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from uuid import UUID
from typing import List, Optional


def get_transaction(db: Session, transaction_id: UUID, user_id: UUID):
    return db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == user_id
    ).first()


def get_transactions(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).offset(skip).limit(limit).all()


def create_transaction(db: Session, transaction_in: TransactionCreate, user_id: UUID):
    db_transaction = Transaction(
        **transaction_in.dict(),
        user_id=user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(db: Session, transaction_id: UUID, user_id: UUID, transaction_in: TransactionUpdate):
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return None
    update_data = transaction_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: UUID, user_id: UUID):
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return False
    db.delete(db_transaction)
    db.commit()
    return True