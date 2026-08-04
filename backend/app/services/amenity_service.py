from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.fleet_master import AmenityMaster
from app.repositories.amenity_repository import (
    create_amenity,
    get_amenities_by_ids,
    get_amenity_by_code,
    get_amenity_by_id,
    get_bus_by_id,
    list_amenities,
    save_amenity,
    save_bus_amenities,
)
from app.schemas.master import AmenityCreate, AmenityUpdate


def get_all_amenities(
    db: Session,
    active_only: bool = True,
):
    return list_amenities(db, active_only)


def add_amenity(
    db: Session,
    payload: AmenityCreate,
):
    normalized_code = payload.code.strip().upper()

    existing = get_amenity_by_code(db, normalized_code)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Amenity code already exists.",
        )

    amenity = AmenityMaster(
        code=normalized_code,
        name=payload.name.strip(),
        description=(
            payload.description.strip()
            if payload.description
            else None
        ),
        display_order=payload.display_order,
        is_active=payload.is_active,
    )

    return create_amenity(db, amenity)


def update_amenity(
    db: Session,
    amenity_id: int,
    payload: AmenityUpdate,
):
    amenity = get_amenity_by_id(db, amenity_id)

    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Amenity not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] is not None:
        amenity.name = update_data["name"].strip()

    if "description" in update_data:
        amenity.description = (
            update_data["description"].strip()
            if update_data["description"]
            else None
        )

    if "display_order" in update_data:
        amenity.display_order = update_data["display_order"]

    if "is_active" in update_data:
        amenity.is_active = update_data["is_active"]

    return save_amenity(db, amenity)


def deactivate_amenity(
    db: Session,
    amenity_id: int,
):
    amenity = get_amenity_by_id(db, amenity_id)

    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Amenity not found.",
        )

    amenity.is_active = False
    return save_amenity(db, amenity)


def get_bus_amenities(
    db: Session,
    bus_id: int,
):
    bus = get_bus_by_id(db, bus_id)

    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found.",
        )

    return bus.amenities


def assign_bus_amenities(
    db: Session,
    bus_id: int,
    amenity_ids: list[int],
):
    bus = get_bus_by_id(db, bus_id)

    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found.",
        )

    unique_ids = list(dict.fromkeys(amenity_ids))
    amenities = get_amenities_by_ids(db, unique_ids)

    found_ids = {amenity.id for amenity in amenities}
    missing_ids = [
        amenity_id
        for amenity_id in unique_ids
        if amenity_id not in found_ids
    ]

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Some amenities are invalid or inactive.",
                "amenity_ids": missing_ids,
            },
        )

    bus.amenities = amenities
    save_bus_amenities(db, bus)

    return bus.amenities


def remove_bus_amenity(
    db: Session,
    bus_id: int,
    amenity_id: int,
):
    bus = get_bus_by_id(db, bus_id)

    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found.",
        )

    amenity = next(
        (
            item
            for item in bus.amenities
            if item.id == amenity_id
        ),
        None,
    )

    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Amenity is not assigned to this bus.",
        )

    bus.amenities.remove(amenity)
    save_bus_amenities(db, bus)

    return bus.amenities