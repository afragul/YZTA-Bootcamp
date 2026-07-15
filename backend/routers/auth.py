from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import create_access_token, verify_password
from crud import users as user_crud
from database import get_db
from dependencies import get_current_user
from models.user import User
from schemas.api_contract import AuthTokenResponse, RegisterRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserResponse:
    email = payload.email.lower().strip()
    if user_crud.get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Bu e-posta adresi zaten kayitli.")
    user = user_crud.create_user(db, email=email, password=payload.password)
    return UserResponse(id=user.id, email=user.email)


@router.post("/login", response_model=AuthTokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> AuthTokenResponse:
    email = form_data.username.lower().strip()
    user = user_crud.get_user_by_email(db, email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="E-posta veya sifre hatali.")
    token = create_access_token(subject=user.email)
    return AuthTokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(id=current_user.id, email=current_user.email)
