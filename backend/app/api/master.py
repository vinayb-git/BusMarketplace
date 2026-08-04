from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.master import MasterDataResponse
from app.services.master_service import (
    list_bus_classes,
    list_bus_configurations,
    list_bus_types,
    list_fuel_types,
    list_service_categories,
)

from app.schemas.master import (
    AmenityCreate,
    AmenityUpdate,
    MasterDataResponse,
)
from app.services.amenity_service import (
    add_amenity,
    deactivate_amenity,
    get_all_amenities,
    update_amenity,
)

router = APIRouter(
    prefix="/master",
    tags=["Master Data"],
)


@router.get(
    "/bus-types",
    response_model=List[MasterDataResponse],
)
def get_bus_types(
    db: Session = Depends(get_db),
):
    return list_bus_types(db)


@router.get(
    "/bus-configurations",
    response_model=List[MasterDataResponse],
)
def get_bus_configurations(
    db: Session = Depends(get_db),
):
    return list_bus_configurations(db)


@router.get(
    "/fuel-types",
    response_model=List[MasterDataResponse],
)
def get_fuel_types(
    db: Session = Depends(get_db),
):
    return list_fuel_types(db)


@router.get(
    "/service-categories",
    response_model=List[MasterDataResponse],
)
def get_service_categories(
    db: Session = Depends(get_db),
):
    return list_service_categories(db)


@router.get(
    "/bus-classes",
    response_model=List[MasterDataResponse],
)
def get_bus_classes(
    db: Session = Depends(get_db),
):
    return list_bus_classes(db)

@router.get(
    "/amenities",
    response_model=list[MasterDataResponse],
)
def list_amenities_endpoint(
    active_only: bool = Query(default=True),
    db: Session = Depends(get_db),
):
    return get_all_amenities(db, active_only)


@router.post(
    "/amenities",
    response_model=MasterDataResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_amenity_endpoint(
    payload: AmenityCreate,
    db: Session = Depends(get_db),
):
    return add_amenity(db, payload)


@router.put(
    "/amenities/{amenity_id}",
    response_model=MasterDataResponse,
)
def update_amenity_endpoint(
    amenity_id: int,
    payload: AmenityUpdate,
    db: Session = Depends(get_db),
):
    return update_amenity(db, amenity_id, payload)


@router.delete(
    "/amenities/{amenity_id}",
    response_model=MasterDataResponse,
)
def deactivate_amenity_endpoint(
    amenity_id: int,
    db: Session = Depends(get_db),
):
    return deactivate_amenity(db, amenity_id)