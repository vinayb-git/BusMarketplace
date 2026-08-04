from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.bus import Bus
from app.models.operator import Operator
from app.models.seat_layout import (
    SeatLayoutTemplate,
    SeatLayoutTemplateSeat,
)


def get_operator_by_id(
    db: Session,
    operator_id: int,
) -> Operator | None:
    return db.get(Operator, operator_id)


def get_template_by_id(
    db: Session,
    template_id: int,
) -> SeatLayoutTemplate | None:
    statement = (
        select(SeatLayoutTemplate)
        .options(selectinload(SeatLayoutTemplate.seats))
        .where(SeatLayoutTemplate.id == template_id)
    )
    return db.scalar(statement)


def get_template_by_code(
    db: Session,
    code: str,
) -> SeatLayoutTemplate | None:
    statement = select(SeatLayoutTemplate).where(
        SeatLayoutTemplate.code == code,
    )
    return db.scalar(statement)


def list_templates(
    db: Session,
    operator_id: int | None = None,
):
    statement = (
        select(SeatLayoutTemplate)
        .options(selectinload(SeatLayoutTemplate.seats))
        .order_by(SeatLayoutTemplate.name)
    )

    if operator_id is not None:
        statement = statement.where(
            SeatLayoutTemplate.operator_id == operator_id,
        )

    return list(db.scalars(statement).unique().all())


def save_template(
    db: Session,
    template: SeatLayoutTemplate,
) -> SeatLayoutTemplate:
    db.add(template)
    db.commit()
    db.refresh(template)
    return get_template_by_id(db, template.id)


def get_seat_by_id(
    db: Session,
    seat_id: int,
) -> SeatLayoutTemplateSeat | None:
    return db.get(SeatLayoutTemplateSeat, seat_id)


def delete_seat(
    db: Session,
    seat: SeatLayoutTemplateSeat,
) -> None:
    db.delete(seat)
    db.commit()


def get_bus_by_id(
    db: Session,
    bus_id: int,
) -> Bus | None:
    return db.get(Bus, bus_id)


def save_bus(
    db: Session,
    bus: Bus,
) -> Bus:
    db.commit()
    db.refresh(bus)
    return bus

def delete_template_seats(
    db: Session,
    template: SeatLayoutTemplate,
) -> None:
    template.seats.clear()
    db.flush()