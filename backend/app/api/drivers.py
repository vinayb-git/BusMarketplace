from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.driver import (
    DriverCreate,
    DriverResponse,
    DriverUpdate,
)
from app.services.driver_service import (
    create_driver,
    deactivate_driver,
    get_all_drivers,
    get_driver,
    update_driver,
)

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
)


@router.get(
    "",
    response_model=list[DriverResponse],
)
def list_drivers_endpoint(
    operator_id: int | None = Query(default=None),
    assigned_bus_id: int | None = Query(default=None),
    active_only: bool = Query(default=True),
    db: Session = Depends(get_db),
):
    return get_all_drivers(
        db,
        operator_id=operator_id,
        assigned_bus_id=assigned_bus_id,
        active_only=active_only,
    )


@router.get(
    "/{driver_id}",
    response_model=DriverResponse,
)
def get_driver_endpoint(
    driver_id: int,
    db: Session = Depends(get_db),
):
    return get_driver(db, driver_id)


@router.post(
    "",
    response_model=DriverResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_driver_endpoint(
    payload: DriverCreate,
    db: Session = Depends(get_db),
):
    return create_driver(db, payload)


@router.put(
    "/{driver_id}",
    response_model=DriverResponse,
)
def update_driver_endpoint(
    driver_id: int,
    payload: DriverUpdate,
    db: Session = Depends(get_db),
):
    return update_driver(
        db,
        driver_id,
        payload,
    )


@router.delete(
    "/{driver_id}",
    response_model=DriverResponse,
)
def deactivate_driver_endpoint(
    driver_id: int,
    db: Session = Depends(get_db),
):
    return deactivate_driver(db, driver_id)