from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User, UserRole


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email.lower())
    return db.scalar(statement)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    return db.scalar(statement)


def get_user_by_phone(db: Session, phone: str) -> User | None:
    statement = select(User).where(User.phone == phone)
    return db.scalar(statement)


def create_user(
    db: Session,
    *,
    first_name: str,
    last_name: str,
    email: str,
    phone: str | None,
    password_hash: str,
    role: UserRole = UserRole.CUSTOMER,
) -> User:
    user = User(
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        email=email.lower().strip(),
        phone=phone.strip() if phone else None,
        password_hash=password_hash,
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user