from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.driver import Driver
from app.repositories.driver_repository import (
    get_bus_by_id,
    get_driver_by_id,
    get_driver_by_license,
    get_operator_by_id,
    list_drivers,
    save_driver,
)
from app.schemas.driver import (
    DriverCreate,
    DriverUpdate,
)


def get_all_drivers(
    db: Session,
    operator_id: int | None = None,
    assigned_bus_id: int | None = None,
    active_only: bool = True,
):
    return list_drivers(
        db,
        operator_id=operator_id,
        assigned_bus_id=assigned_bus_id,
        active_only=active_only,
    )


def get_driver(
    db: Session,
    driver_id: int,
) -> Driver:
    driver = get_driver_by_id(db, driver_id)

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found.",
        )

    return driver


def _validate_license_dates(
    issue_date: date | None,
    expiry_date: date,
) -> None:
    if issue_date and issue_date > expiry_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "License issue date cannot be after "
                "license expiry date."
            ),
        )


def _validate_bus_assignment(
    db: Session,
    operator_id: int,
    bus_id: int | None,
) -> None:
    if bus_id is None:
        return

    bus = get_bus_by_id(db, bus_id)

    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned bus not found.",
        )

    if bus.operator_id != operator_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Driver and assigned bus must belong "
                "to the same operator."
            ),
        )


def create_driver(
    db: Session,
    payload: DriverCreate,
) -> Driver:
    operator = get_operator_by_id(db, payload.operator_id)

    if not operator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator not found.",
        )

    normalized_license = payload.license_number.strip().upper()

    if get_driver_by_license(
        db,
        payload.operator_id,
        normalized_license,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "A driver with this license number "
                "already exists for this operator."
            ),
        )

    _validate_license_dates(
        payload.license_issue_date,
        payload.license_expiry_date,
    )

    _validate_bus_assignment(
        db,
        payload.operator_id,
        payload.assigned_bus_id,
    )

    driver = Driver(
        operator_id=payload.operator_id,
        assigned_bus_id=payload.assigned_bus_id,
        employee_code=(
            payload.employee_code.strip()
            if payload.employee_code
            else None
        ),
        first_name=payload.first_name.strip(),
        last_name=(
            payload.last_name.strip()
            if payload.last_name
            else None
        ),
        phone_number=payload.phone_number.strip(),
        alternate_phone_number=(
            payload.alternate_phone_number.strip()
            if payload.alternate_phone_number
            else None
        ),
        email=str(payload.email) if payload.email else None,
        date_of_birth=payload.date_of_birth,
        blood_group=(
            payload.blood_group.strip().upper()
            if payload.blood_group
            else None
        ),
        address=(
            payload.address.strip()
            if payload.address
            else None
        ),
        emergency_contact_name=(
            payload.emergency_contact_name.strip()
            if payload.emergency_contact_name
            else None
        ),
        emergency_contact_phone=(
            payload.emergency_contact_phone.strip()
            if payload.emergency_contact_phone
            else None
        ),
        license_number=normalized_license,
        license_type=(
            payload.license_type.strip().upper()
            if payload.license_type
            else None
        ),
        license_issue_date=payload.license_issue_date,
        license_expiry_date=payload.license_expiry_date,
        government_id_type=(
            payload.government_id_type.strip().upper()
            if payload.government_id_type
            else None
        ),
        government_id_number=(
            payload.government_id_number.strip()
            if payload.government_id_number
            else None
        ),
        years_of_experience=payload.years_of_experience,
        status=payload.status,
        is_available=payload.is_available,
        is_active=payload.is_active,
        notes=(
            payload.notes.strip()
            if payload.notes
            else None
        ),
    )

    try:
        return save_driver(db, driver)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Driver data conflicts with an existing record.",
        )


def update_driver(
    db: Session,
    driver_id: int,
    payload: DriverUpdate,
) -> Driver:
    driver = get_driver(db, driver_id)
    update_data = payload.model_dump(exclude_unset=True)

    new_issue_date = update_data.get(
        "license_issue_date",
        driver.license_issue_date,
    )
    new_expiry_date = update_data.get(
        "license_expiry_date",
        driver.license_expiry_date,
    )

    _validate_license_dates(
        new_issue_date,
        new_expiry_date,
    )

    if "assigned_bus_id" in update_data:
        _validate_bus_assignment(
            db,
            driver.operator_id,
            update_data["assigned_bus_id"],
        )

    string_fields = {
        "employee_code",
        "first_name",
        "last_name",
        "phone_number",
        "alternate_phone_number",
        "blood_group",
        "address",
        "emergency_contact_name",
        "emergency_contact_phone",
        "license_type",
        "government_id_type",
        "government_id_number",
        "notes",
    }

    uppercase_fields = {
        "blood_group",
        "license_type",
        "government_id_type",
    }

    for field, value in update_data.items():
        if field == "email" and value is not None:
            value = str(value)

        if field in string_fields and isinstance(value, str):
            value = value.strip()

        if field in uppercase_fields and isinstance(value, str):
            value = value.upper()

        setattr(driver, field, value)

    try:
        return save_driver(db, driver)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Driver data conflicts with an existing record.",
        )


def deactivate_driver(
    db: Session,
    driver_id: int,
) -> Driver:
    driver = get_driver(db, driver_id)

    driver.is_active = False
    driver.is_available = False
    driver.assigned_bus_id = None

    return save_driver(db, driver)