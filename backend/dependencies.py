from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth import decode_access_token
from crud import users as user_crud
from database import get_db
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_current_user_optional(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    if not token:
        return None
    email = decode_access_token(token)
    if not email:
        return None
    return user_crud.get_user_by_email(db, email)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Giris yapmaniz gerekiyor.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = decode_access_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Gecersiz veya suresi dolmus token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanici bulunamadi.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
