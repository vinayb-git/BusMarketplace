from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.driver import DriverStatus


class DriverCreate(BaseModel):
    operator_id: int
    assigned_bus_id: int | None = None

    employee_code: str | None = Field(default=None, max_length=50)

    first_name: str = Field(min_length=2, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)

    phone_number: str = Field(max_length=20)
    alternate_phone_number: str | None = Field(default=None, max_length=20)

    email: EmailStr | None = None

    date_of_birth: date | None = None
    blood_group: str | None = None
    address: str | None = None

    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None

    license_number: str = Field(max_length=100)
    license_type: str | None = None
    license_issue_date: date | None = None
    license_expiry_date: date

    government_id_type: str | None = None
    government_id_number: str | None = None

    years_of_experience: int = Field(default=0, ge=0)

    status: DriverStatus = DriverStatus.ACTIVE
    is_available: bool = True
    is_active: bool = True

    notes: str | None = None

class DriverUpdate(BaseModel):
    assigned_bus_id: int | None = None

    employee_code: str | None = None

    first_name: str | None = None
    last_name: str | None = None

    phone_number: str | None = None
    alternate_phone_number: str | None = None

    email: EmailStr | None = None

    date_of_birth: date | None = None
    blood_group: str | None = None
    address: str | None = None

    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None

    license_type: str | None = None
    license_issue_date: date | None = None
    license_expiry_date: date | None = None

    government_id_type: str | None = None
    government_id_number: str | None = None

    years_of_experience: int | None = Field(default=None, ge=0)

    status: DriverStatus | None = None
    is_available: bool | None = None
    is_active: bool | None = None

    notes: str | None = None

class DriverResponse(BaseModel):
    id: int

    operator_id: int
    assigned_bus_id: int | None

    employee_code: str | None

    first_name: str
    last_name: str | None

    phone_number: str
    alternate_phone_number: str | None

    email: EmailStr | None

    date_of_birth: date | None
    blood_group: str | None
    address: str | None

    emergency_contact_name: str | None
    emergency_contact_phone: str | None

    license_number: str
    license_type: str | None
    license_issue_date: date | None
    license_expiry_date: date

    government_id_type: str | None
    government_id_number: str | None

    years_of_experience: int

    status: DriverStatus

    is_available: bool
    is_active: bool

    notes: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)