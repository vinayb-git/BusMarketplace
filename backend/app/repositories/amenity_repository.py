from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bus import Bus
from app.models.fleet_master import AmenityMaster


def list_amenities(db: Session, active_only: bool = True):
    statement = select(AmenityMaster)

    if active_only:
        statement = statement.where(AmenityMaster.is_active.is_(True))

    statement = statement.order_by(
        AmenityMaster.display_order,
        AmenityMaster.name,
    )

    return list(db.scalars(statement).all())


def get_amenity_by_id(
    db: Session,
    amenity_id: int,
) -> AmenityMaster | None:
    return db.get(AmenityMaster, amenity_id)


def get_amenity_by_code(
    db: Session,
    code: str,
) -> AmenityMaster | None:
    statement = select(AmenityMaster).where(
        AmenityMaster.code == code,
    )
    return db.scalar(statement)


def create_amenity(
    db: Session,
    amenity: AmenityMaster,
) -> AmenityMaster:
    db.add(amenity)
    db.commit()
    db.refresh(amenity)
    return amenity


def save_amenity(
    db: Session,
    amenity: AmenityMaster,
) -> AmenityMaster:
    db.commit()
    db.refresh(amenity)
    return amenity


def get_bus_by_id(
    db: Session,
    bus_id: int,
) -> Bus | None:
    return db.get(Bus, bus_id)


def get_amenities_by_ids(
    db: Session,
    amenity_ids: list[int],
) -> list[AmenityMaster]:
    statement = select(AmenityMaster).where(
        AmenityMaster.id.in_(amenity_ids),
        AmenityMaster.is_active.is_(True),
    )
    return list(db.scalars(statement).all())


def save_bus_amenities(
    db: Session,
    bus: Bus,
) -> Bus:
    db.commit()
    db.refresh(bus)
    return bus