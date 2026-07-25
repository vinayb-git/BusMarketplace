from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.operator import Operator, OperatorStatus
from app.models.user import User, UserRole
from app.repositories.location_repository import get_city_by_id
from app.repositories.operator_repository import (
    change_operator_status,
    create_operator,
    get_operator_by_id,
    get_operator_by_owner,
    get_operator_by_registration_number,
    get_operator_by_tax_id,
)
from app.schemas.operator import OperatorCreate


def register_operator(
    db: Session,
    *,
    current_user: User,
    request: OperatorCreate,
) -> Operator:
    if get_operator_by_owner(db, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already owns an operator account.",
        )

    if not get_city_by_id(db, request.city_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found.",
        )

    if (
        request.registration_number
        and get_operator_by_registration_number(
            db,
            request.registration_number.strip(),
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registration number already exists.",
        )

    if request.tax_id and get_operator_by_tax_id(
        db,
        request.tax_id.strip(),
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tax ID already exists.",
        )

    try:
        operator = create_operator(
            db,
            owner_user_id=current_user.id,
            request=request,
        )

        if current_user.role == UserRole.CUSTOMER:
            current_user.role = UserRole.OPERATOR
            db.commit()

        return operator

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Operator information conflicts with an existing record.",
        )


def get_accessible_operator(
    db: Session,
    *,
    operator_id: int,
    current_user: User,
) -> Operator:
    operator = get_operator_by_id(db, operator_id)

    if operator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator not found.",
        )

    if (
        current_user.role != UserRole.ADMIN
        and operator.owner_user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this operator.",
        )

    return operator


def approve_operator(
    db: Session,
    operator: Operator,
) -> Operator:
    return change_operator_status(
        db,
        operator=operator,
        new_status=OperatorStatus.APPROVED,
        rejection_reason=None,
    )


def reject_operator(
    db: Session,
    operator: Operator,
    reason: str,
) -> Operator:
    return change_operator_status(
        db,
        operator=operator,
        new_status=OperatorStatus.REJECTED,
        rejection_reason=reason.strip(),
    )


def suspend_operator(
    db: Session,
    operator: Operator,
) -> Operator:
    return change_operator_status(
        db,
        operator=operator,
        new_status=OperatorStatus.SUSPENDED,
        rejection_reason=None,
    )