from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas

def get_all_transactions(db: Session, user_id: int):
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id
    ).all()

def get_transaction_by_id(db: Session, transaction_id: int, user_id: int):
    return db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()

def create_transaction(db: Session, data: schemas.TransactionCreate, user_id: int):
    if data.type not in ["income", "expense"]:
        return None, "Type must be 'income' or 'expense'"
    if data.amount <= 0:
        return None, "Amount must be greater than zero"
    transaction = models.Transaction(
        title=data.title,
        amount=data.amount,
        type=data.type,
        category=data.category,
        date=data.date or datetime.utcnow(),
        user_id=user_id
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction, None

def update_transaction(db: Session, transaction_id: int, data: schemas.TransactionUpdate, user_id: int):
    transaction = get_transaction_by_id(db, transaction_id, user_id)
    if not transaction:
        return None, "Transaction not found"
    if data.type is not None and data.type not in ["income", "expense"]:
        return None, "Type must be 'income' or 'expense'"
    if data.amount is not None and data.amount <= 0:
        return None, "Amount must be greater than zero"
    if data.title is not None:
        transaction.title = data.title
    if data.amount is not None:
        transaction.amount = data.amount
    if data.type is not None:
        transaction.type = data.type
    if data.category is not None:
        transaction.category = data.category
    if data.date is not None:
        transaction.date = data.date
    db.commit()
    db.refresh(transaction)
    return transaction, None

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    transaction = get_transaction_by_id(db, transaction_id, user_id)
    if not transaction:
        return None, "Transaction not found"
    db.delete(transaction)
    db.commit()
    return transaction, None

def get_summary(db: Session, user_id: int):
    transactions = get_all_transactions(db, user_id)
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    balance = total_income - total_expense
    return schemas.SummaryResponse(
        total_income=total_income,
        total_expense=total_expense,
        balance=balance
    )