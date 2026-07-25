from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_phone,
)
from app.schemas.user import UserCreate


def register_user(db: Session, request: UserCreate) -> User:
    normalized_email = request.email.lower().strip()

    if get_user_by_email(db, normalized_email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    if request.phone and get_user_by_phone(db, request.phone.strip()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this phone number already exists.",
        )

    try:
        return create_user(
            db,
            first_name=request.first_name,
            last_name=request.last_name,
            email=normalized_email,
            phone=request.phone,
            password_hash=hash_password(request.password),
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with the provided information already exists.",
        )


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> tuple[User, str]:
    user = get_user_by_email(db, email.lower().strip())

    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive.",
        )

    access_token = create_access_token(subject=user.id)

    return user, access_token