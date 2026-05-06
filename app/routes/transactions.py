from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from app import schemas, models
from app.services import transactions as transaction_service
from app.database import get_db
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/transactions", tags=["Transactions"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/summary", response_model=schemas.SummaryResponse)
def get_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return transaction_service.get_summary(db, current_user.id)

@router.get("/", response_model=list[schemas.TransactionResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return transaction_service.get_all_transactions(db, current_user.id)

@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_one(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    transaction = transaction_service.get_transaction_by_id(db, transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/", response_model=schemas.TransactionResponse, status_code=201)
def create(
    data: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    transaction, error = transaction_service.create_transaction(db, data, current_user.id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return transaction

@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update(
    transaction_id: int,
    data: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    transaction, error = transaction_service.update_transaction(db, transaction_id, data, current_user.id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return transaction

@router.delete("/{transaction_id}")
def delete(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    transaction, error = transaction_service.delete_transaction(db, transaction_id, current_user.id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return {"message": "Transaction deleted successfully", "deleted": transaction.title}