from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# --- Auth ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Transactions ---
class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str  # "income" ou "expense"
    category: Optional[str] = "general"
    date: Optional[datetime] = None

class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None

class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    category: str
    date: datetime
    user_id: int

    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float