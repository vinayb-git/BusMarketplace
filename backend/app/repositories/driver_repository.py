from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bus import Bus
from app.models.driver import Driver
from app.models.operator import Operator


def get_operator_by_id(
    db: Session,
    operator_id: int,
) -> Operator | None:
    return db.get(Operator, operator_id)


def get_bus_by_id(
    db: Session,
    bus_id: int,
) -> Bus | None:
    return db.get(Bus, bus_id)


def get_driver_by_id(
    db: Session,
    driver_id: int,
) -> Driver | None:
    return db.get(Driver, driver_id)


def get_driver_by_license(
    db: Session,
    operator_id: int,
    license_number: str,
) -> Driver | None:
    statement = select(Driver).where(
        Driver.operator_id == operator_id,
        Driver.license_number == license_number,
    )
    return db.scalar(statement)


def list_drivers(
    db: Session,
    operator_id: int | None = None,
    assigned_bus_id: int | None = None,
    active_only: bool = True,
):
    statement = select(Driver).order_by(
        Driver.first_name,
        Driver.last_name,
    )

    if operator_id is not None:
        statement = statement.where(
            Driver.operator_id == operator_id,
        )

    if assigned_bus_id is not None:
        statement = statement.where(
            Driver.assigned_bus_id == assigned_bus_id,
        )

    if active_only:
        statement = statement.where(
            Driver.is_active.is_(True),
        )

    return list(db.scalars(statement).all())


def save_driver(
    db: Session,
    driver: Driver,
) -> Driver:
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver