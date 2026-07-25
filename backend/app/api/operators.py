from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_admin
from app.database.session import get_db
from app.models.operator import OperatorStatus
from app.models.user import User
from app.repositories.operator_repository import (
    create_operator_bank_account,
    create_operator_contact,
    list_operators,
    update_operator,
)
from app.schemas.operator import (
    OperatorBankAccountCreate,
    OperatorBankAccountResponse,
    OperatorContactCreate,
    OperatorContactResponse,
    OperatorCreate,
    OperatorDetailResponse,
    OperatorRejectRequest,
    OperatorResponse,
    OperatorUpdate,
)
from app.services.operator_service import (
    approve_operator,
    get_accessible_operator,
    register_operator,
    reject_operator,
    suspend_operator,
)


router = APIRouter(
    prefix="/operators",
    tags=["Operators"],
)


@router.post(
    "",
    response_model=OperatorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_operator(
    request: OperatorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return register_operator(
        db,
        current_user=current_user,
        request=request,
    )


@router.get(
    "",
    response_model=list[OperatorResponse],
)
def get_all_operators(
    status_filter: OperatorStatus | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return list_operators(db, status_filter)


@router.get(
    "/{operator_id}",
    response_model=OperatorDetailResponse,
)
def get_operator(
    operator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_accessible_operator(
        db,
        operator_id=operator_id,
        current_user=current_user,
    )


@router.put(
    "/{operator_id}",
    response_model=OperatorResponse,
)
def modify_operator(
    operator_id: int,
    request: OperatorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    operator = get_accessible_operator(
        db,
        operator_id=operator_id,
        current_user=current_user,
    )

    return update_operator(
        db,
        operator=operator,
        request=request,
    )


@router.post(
    "/{operator_id}/contacts",
    response_model=OperatorContactResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_contact(
    operator_id: int,
    request: OperatorContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_accessible_operator(
        db,
        operator_id=operator_id,
        current_user=current_user,
    )

    return create_operator_contact(
        db,
        operator_id=operator_id,
        full_name=request.full_name,
        job_title=request.job_title,
        email=request.email,
        phone=request.phone,
        is_primary=request.is_primary,
    )


@router.post(
    "/{operator_id}/bank-accounts",
    response_model=OperatorBankAccountResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_bank_account(
    operator_id: int,
    request: OperatorBankAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_accessible_operator(
        db,
        operator_id=operator_id,
        current_user=current_user,
    )

    return create_operator_bank_account(
        db,
        operator_id=operator_id,
        account_name=request.account_name,
        account_number=request.account_number,
        bank_name=request.bank_name,
        routing_code=request.routing_code,
        account_type=request.account_type,
        is_primary=request.is_primary,
    )


@router.patch(
    "/{operator_id}/approve",
    response_model=OperatorResponse,
)
def approve(
    operator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    operator = get_accessible_operator(
        db,
        operator_id=operator_id,
        current_user=current_user,
    )

    return approve_operator(db, operator)


@router.patch(
    "/{operator_id}/reject",
    response_model=OperatorResponse,
)
def reject(
    operator_id: int,
    request: OperatorRejectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    operator = get_accessible_operator(
        db,
        operator_id=operator_id,
        current_user=current_user,
    )

    return reject_operator(
        db,
        operator,
        request.reason,
    )


@router.patch(
    "/{operator_id}/suspend",
    response_model=OperatorResponse,
)
def suspend(
    operator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    operator = get_accessible_operator(
        db,
        operator_id=operator_id,
        current_user=current_user,
    )

    return suspend_operator(db, operator)