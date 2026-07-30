from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.bus import Bus, BusStatus
from app.models.operator import Operator, OperatorStatus
from app.models.user import User, UserRole
from app.repositories.bus_repository import (
    create_bus,
    deactivate_bus,
    get_bus_by_id,
    get_bus_by_operator_and_fleet_number,
    get_bus_by_registration_number,
    set_bus_status,
    update_bus,
)
from app.repositories.operator_repository import (
    get_operator_by_id,
    get_operator_by_owner,
)
from app.schemas.bus import BusCreate, BusUpdate


def get_operator_for_fleet_access(
    db: Session,
    *,
    current_user: User,
    operator_id: int | None = None,
    require_approved: bool = False,
) -> Operator:
    if current_user.role == UserRole.ADMIN:
        if operator_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="operator_id is required for administrator requests.",
            )

        operator = get_operator_by_id(db, operator_id)

    else:
        operator = get_operator_by_owner(db, current_user.id)

        if (
            operator_id is not None
            and operator is not None
            and operator.id != operator_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this operator's fleet.",
            )

    if operator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator account not found.",
        )

    if not operator.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator account is inactive.",
        )

    if (
        require_approved
        and operator.status != OperatorStatus.APPROVED
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator must be approved before managing buses.",
        )

    return operator


def create_operator_bus(
    db: Session,
    *,
    operator: Operator,
    request: BusCreate,
) -> Bus:
    existing = get_bus_by_registration_number(
        db,
        request.registration_number,
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A bus with this registration number already exists.",
        )

    if request.fleet_number:
        existing_fleet = get_bus_by_operator_and_fleet_number(
            db,
            operator_id=operator.id,
            fleet_number=request.fleet_number,
        )

        if existing_fleet:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This fleet number already exists for the operator.",
            )

    current_year = datetime.now(timezone.utc).year

    if (
        request.manufacturing_year
        and request.manufacturing_year > current_year + 1
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Manufacturing year cannot be more than "
                "one year in the future."
            ),
        )

    try:
        return create_bus(
            db,
            operator_id=operator.id,
            request=request,
        )

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bus information conflicts with an existing record.",
        ) from exc


def get_accessible_bus(
    db: Session,
    *,
    bus_id: int,
    current_user: User,
) -> Bus:
    bus = get_bus_by_id(db, bus_id)

    if bus is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found.",
        )

    if current_user.role != UserRole.ADMIN:
        operator = get_operator_by_owner(db, current_user.id)

        if operator is None or bus.operator_id != operator.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this bus.",
            )

    return bus


def modify_bus(
    db: Session,
    *,
    bus: Bus,
    request: BusUpdate,
) -> Bus:
    if request.fleet_number:
        existing = get_bus_by_operator_and_fleet_number(
            db,
            operator_id=bus.operator_id,
            fleet_number=request.fleet_number,
        )

        if existing and existing.id != bus.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This fleet number already exists for the operator.",
            )

    current_year = datetime.now(timezone.utc).year

    if (
        request.manufacturing_year
        and request.manufacturing_year > current_year + 1
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Manufacturing year cannot be more than "
                "one year in the future."
            ),
        )

    try:
        return update_bus(
            db,
            bus=bus,
            request=request,
        )

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bus information conflicts with an existing record.",
        ) from exc


def change_bus_status(
    db: Session,
    *,
    bus: Bus,
    new_status: BusStatus,
) -> Bus:
    if (
        bus.status == BusStatus.RETIRED
        and new_status != BusStatus.RETIRED
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A retired bus cannot be reactivated directly.",
        )

    return set_bus_status(
        db,
        bus=bus,
        new_status=new_status,
    )


def remove_bus(
    db: Session,
    *,
    bus: Bus,
) -> Bus:
    if bus.status == BusStatus.RETIRED:
        return bus

    return deactivate_bus(db, bus)