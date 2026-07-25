from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.session import get_db
from app.models.user import User
from app.repositories.user_repository import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    subject = payload.get("sub")

    if subject is None:
        raise credentials_exception

    try:
        user_id = int(subject)
    except (TypeError, ValueError):
        raise credentials_exception

    user = get_user_by_id(db, user_id)

    if user is None or not user.is_active:
        raise credentials_exception

    return user