from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.operator import (
    Operator,
    OperatorBankAccount,
    OperatorContact,
    OperatorStatus,
)
from app.schemas.operator import OperatorCreate, OperatorUpdate


def get_operator_by_id(
    db: Session,
    operator_id: int,
) -> Operator | None:
    statement = (
        select(Operator)
        .options(
            selectinload(Operator.contacts),
            selectinload(Operator.bank_accounts),
        )
        .where(Operator.id == operator_id)
    )

    return db.scalar(statement)


def get_operator_by_owner(
    db: Session,
    owner_user_id: int,
) -> Operator | None:
    statement = select(Operator).where(
        Operator.owner_user_id == owner_user_id
    )

    return db.scalar(statement)


def get_operator_by_registration_number(
    db: Session,
    registration_number: str,
) -> Operator | None:
    statement = select(Operator).where(
        Operator.registration_number == registration_number
    )

    return db.scalar(statement)


def get_operator_by_tax_id(
    db: Session,
    tax_id: str,
) -> Operator | None:
    statement = select(Operator).where(
        Operator.tax_id == tax_id
    )

    return db.scalar(statement)


def list_operators(
    db: Session,
    status_filter: OperatorStatus | None = None,
) -> list[Operator]:
    statement = select(Operator).order_by(Operator.created_at.desc())

    if status_filter is not None:
        statement = statement.where(Operator.status == status_filter)

    return list(db.scalars(statement).all())


def create_operator(
    db: Session,
    *,
    owner_user_id: int,
    request: OperatorCreate,
) -> Operator:
    operator = Operator(
        owner_user_id=owner_user_id,
        legal_name=request.legal_name.strip(),
        display_name=request.display_name.strip(),
        registration_number=(
            request.registration_number.strip()
            if request.registration_number
            else None
        ),
        tax_id=request.tax_id.strip() if request.tax_id else None,
        address_line_1=request.address_line_1.strip(),
        address_line_2=(
            request.address_line_2.strip()
            if request.address_line_2
            else None
        ),
        city_id=request.city_id,
        postal_code=request.postal_code.strip(),
    )

    db.add(operator)
    db.commit()
    db.refresh(operator)

    return operator


def update_operator(
    db: Session,
    *,
    operator: Operator,
    request: OperatorUpdate,
) -> Operator:
    updates = request.model_dump(exclude_unset=True)

    for field, value in updates.items():
        if isinstance(value, str):
            value = value.strip()

        setattr(operator, field, value)

    db.commit()
    db.refresh(operator)

    return operator


def create_operator_contact(
    db: Session,
    *,
    operator_id: int,
    full_name: str,
    job_title: str | None,
    email: str,
    phone: str,
    is_primary: bool,
) -> OperatorContact:
    if is_primary:
        existing_primary = db.scalars(
            select(OperatorContact).where(
                OperatorContact.operator_id == operator_id,
                OperatorContact.is_primary.is_(True),
            )
        ).all()

        for contact in existing_primary:
            contact.is_primary = False

    contact = OperatorContact(
        operator_id=operator_id,
        full_name=full_name.strip(),
        job_title=job_title.strip() if job_title else None,
        email=email.lower().strip(),
        phone=phone.strip(),
        is_primary=is_primary,
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def create_operator_bank_account(
    db: Session,
    *,
    operator_id: int,
    account_name: str,
    account_number: str,
    bank_name: str,
    routing_code: str,
    account_type: str | None,
    is_primary: bool,
) -> OperatorBankAccount:
    if is_primary:
        existing_primary = db.scalars(
            select(OperatorBankAccount).where(
                OperatorBankAccount.operator_id == operator_id,
                OperatorBankAccount.is_primary.is_(True),
            )
        ).all()

        for account in existing_primary:
            account.is_primary = False

    account = OperatorBankAccount(
        operator_id=operator_id,
        account_name=account_name.strip(),
        account_number=account_number.strip(),
        bank_name=bank_name.strip(),
        routing_code=routing_code.strip(),
        account_type=account_type.strip() if account_type else None,
        is_primary=is_primary,
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return account


def change_operator_status(
    db: Session,
    *,
    operator: Operator,
    new_status: OperatorStatus,
    rejection_reason: str | None = None,
) -> Operator:
    operator.status = new_status
    operator.rejection_reason = rejection_reason

    db.commit()
    db.refresh(operator)

    return operator