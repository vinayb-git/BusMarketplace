from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_db
from app.models.bus import BusStatus, BusType, ServiceType
from app.models.user import User, UserRole
from app.repositories.bus_repository import list_buses
from app.schemas.bus import (
    BusCreate,
    BusResponse,
    BusStatusUpdate,
    BusUpdate,
)
from app.services.bus_service import (
    change_bus_status,
    create_operator_bus,
    get_accessible_bus,
    get_operator_for_fleet_access,
    modify_bus,
    remove_bus,
)
from app.schemas.master import (
    BusAmenityAssignment,
    MasterDataResponse,
)
from app.services.amenity_service import (
    assign_bus_amenities,
    get_bus_amenities,
    remove_bus_amenity,
)

router = APIRouter(
    prefix="/buses",
    tags=["Fleet Management"],
)


@router.post(
    "",
    response_model=BusResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_bus(
    request: BusCreate,
    operator_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    operator = get_operator_for_fleet_access(
        db,
        current_user=current_user,
        operator_id=operator_id,
        require_approved=True,
    )

    return create_operator_bus(
        db,
        operator=operator,
        request=request,
    )


@router.get(
    "",
    response_model=list[BusResponse],
)
def get_buses(
    operator_id: int | None = Query(default=None),
    status_filter: BusStatus | None = Query(
        default=None,
        alias="status",
    ),
    bus_type: BusType | None = Query(default=None),
    service_type: ServiceType | None = Query(default=None),
    is_active: bool | None = Query(default=True),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.ADMIN:
        selected_operator_id = operator_id
    else:
        operator = get_operator_for_fleet_access(
            db,
            current_user=current_user,
            operator_id=operator_id,
        )
        selected_operator_id = operator.id

    return list_buses(
        db,
        operator_id=selected_operator_id,
        status_filter=status_filter,
        bus_type=bus_type,
        service_type=service_type,
        is_active=is_active,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{bus_id}",
    response_model=BusResponse,
)
def get_bus(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_accessible_bus(
        db,
        bus_id=bus_id,
        current_user=current_user,
    )


@router.put(
    "/{bus_id}",
    response_model=BusResponse,
)
def update_existing_bus(
    bus_id: int,
    request: BusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bus = get_accessible_bus(
        db,
        bus_id=bus_id,
        current_user=current_user,
    )

    return modify_bus(
        db,
        bus=bus,
        request=request,
    )


@router.patch(
    "/{bus_id}/status",
    response_model=BusResponse,
)
def update_bus_status(
    bus_id: int,
    request: BusStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bus = get_accessible_bus(
        db,
        bus_id=bus_id,
        current_user=current_user,
    )

    return change_bus_status(
        db,
        bus=bus,
        new_status=request.status,
    )


@router.delete(
    "/{bus_id}",
    response_model=BusResponse,
)
def deactivate_existing_bus(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bus = get_accessible_bus(
        db,
        bus_id=bus_id,
        current_user=current_user,
    )

    return remove_bus(
        db,
        bus=bus,
    )
@router.get(
    "/{bus_id}/amenities",
    response_model=list[MasterDataResponse],
)
def get_bus_amenities_endpoint(
    bus_id: int,
    db: Session = Depends(get_db),
):
    return get_bus_amenities(db, bus_id)


@router.put(
    "/{bus_id}/amenities",
    response_model=list[MasterDataResponse],
)
def assign_bus_amenities_endpoint(
    bus_id: int,
    payload: BusAmenityAssignment,
    db: Session = Depends(get_db),
):
    return assign_bus_amenities(
        db,
        bus_id,
        payload.amenity_ids,
    )


@router.delete(
    "/{bus_id}/amenities/{amenity_id}",
    response_model=list[MasterDataResponse],
)
def remove_bus_amenity_endpoint(
    bus_id: int,
    amenity_id: int,
    db: Session = Depends(get_db),
):
    return remove_bus_amenity(
        db,
        bus_id,
        amenity_id,
    )