from sqlalchemy.orm import Session

from app.models.fleet_master import (
    BusClassMaster,
    BusConfigurationMaster,
    BusTypeMaster,
    FuelTypeMaster,
    ServiceCategoryMaster,
)


def get_bus_types(db: Session):
    return (
        db.query(BusTypeMaster)
        .filter(BusTypeMaster.is_active.is_(True))
        .order_by(BusTypeMaster.display_order)
        .all()
    )


def get_bus_configurations(db: Session):
    return (
        db.query(BusConfigurationMaster)
        .filter(BusConfigurationMaster.is_active.is_(True))
        .order_by(BusConfigurationMaster.display_order)
        .all()
    )


def get_fuel_types(db: Session):
    return (
        db.query(FuelTypeMaster)
        .filter(FuelTypeMaster.is_active.is_(True))
        .order_by(FuelTypeMaster.display_order)
        .all()
    )


def get_service_categories(db: Session):
    return (
        db.query(ServiceCategoryMaster)
        .filter(ServiceCategoryMaster.is_active.is_(True))
        .order_by(ServiceCategoryMaster.display_order)
        .all()
    )


def get_bus_classes(db: Session):
    return (
        db.query(BusClassMaster)
        .filter(BusClassMaster.is_active.is_(True))
        .order_by(BusClassMaster.display_order)
        .all()
    )