from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas
from app.services import auth as auth_service
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user, error = auth_service.register_user(db, user_data)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token, error = auth_service.login_user_form(db, form_data.username, form_data.password)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return {"access_token": token, "token_type": "bearer"}