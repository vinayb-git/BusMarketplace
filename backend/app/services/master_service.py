from sqlalchemy.orm import Session

from app.repositories.master_repository import (
    get_bus_classes,
    get_bus_configurations,
    get_bus_types,
    get_fuel_types,
    get_service_categories,
)


def list_bus_types(db: Session):
    return get_bus_types(db)


def list_bus_configurations(db: Session):
    return get_bus_configurations(db)


def list_fuel_types(db: Session):
    return get_fuel_types(db)


def list_service_categories(db: Session):
    return get_service_categories(db)


def list_bus_classes(db: Session):
    return get_bus_classes(db)