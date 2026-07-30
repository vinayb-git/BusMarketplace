from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bus import Bus, BusStatus, BusType, ServiceType
from app.schemas.bus import BusCreate, BusUpdate


def get_bus_by_id(db: Session, bus_id: int) -> Bus | None:
    return db.scalar(select(Bus).where(Bus.id == bus_id))


def get_bus_by_registration_number(
    db: Session,
    registration_number: str,
) -> Bus | None:
    return db.scalar(
        select(Bus).where(
            Bus.registration_number == registration_number.upper().strip()
        )
    )


def get_bus_by_operator_and_fleet_number(
    db: Session,
    *,
    operator_id: int,
    fleet_number: str,
) -> Bus | None:
    return db.scalar(
        select(Bus).where(
            Bus.operator_id == operator_id,
            Bus.fleet_number == fleet_number.strip(),
        )
    )


def list_buses(
    db: Session,
    *,
    operator_id: int | None = None,
    status_filter: BusStatus | None = None,
    bus_type: BusType | None = None,
    service_type: ServiceType | None = None,
    is_active: bool | None = True,
    skip: int = 0,
    limit: int = 50,
) -> list[Bus]:
    statement = select(Bus)

    if operator_id is not None:
        statement = statement.where(Bus.operator_id == operator_id)

    if status_filter is not None:
        statement = statement.where(Bus.status == status_filter)

    if bus_type is not None:
        statement = statement.where(Bus.bus_type == bus_type)

    if service_type is not None:
        statement = statement.where(Bus.service_type == service_type)

    if is_active is not None:
        statement = statement.where(Bus.is_active == is_active)

    statement = (
        statement
        .order_by(Bus.id.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def create_bus(
    db: Session,
    *,
    operator_id: int,
    request: BusCreate,
) -> Bus:
    bus = Bus(
        operator_id=operator_id,
        **request.model_dump(),
    )

    db.add(bus)
    db.commit()
    db.refresh(bus)

    return bus


def update_bus(
    db: Session,
    *,
    bus: Bus,
    request: BusUpdate,
) -> Bus:
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(bus, field, value)

    db.commit()
    db.refresh(bus)

    return bus


def set_bus_status(
    db: Session,
    *,
    bus: Bus,
    new_status: BusStatus,
) -> Bus:
    bus.status = new_status
    bus.is_active = new_status not in {
        BusStatus.INACTIVE,
        BusStatus.RETIRED,
    }

    db.commit()
    db.refresh(bus)

    return bus


def deactivate_bus(db: Session, bus: Bus) -> Bus:
    bus.is_active = False
    bus.status = BusStatus.INACTIVE

    db.commit()
    db.refresh(bus)

    return bus