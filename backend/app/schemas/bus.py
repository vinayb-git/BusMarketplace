from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.bus import BusStatus, BusType, FuelType, ServiceType


class BusBase(BaseModel):
    registration_number: str = Field(min_length=3, max_length=50)
    fleet_number: str | None = Field(default=None, max_length=50)
    bus_name: str = Field(min_length=2, max_length=150)
    bus_type: BusType
    service_type: ServiceType
    fuel_type: FuelType = FuelType.DIESEL
    manufacturer: str | None = Field(default=None, max_length=100)
    model_name: str | None = Field(default=None, max_length=100)
    manufacturing_year: int | None = Field(default=None, ge=1980, le=2100)
    total_capacity: int = Field(ge=1, le=200)
    number_of_decks: int = Field(default=1, ge=1, le=2)
    has_air_conditioning: bool = False

    @field_validator(
        "registration_number",
        "fleet_number",
        "bus_name",
        "manufacturer",
        "model_name",
        mode="before",
    )
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    @field_validator("registration_number")
    @classmethod
    def normalize_registration_number(cls, value: str) -> str:
        return value.upper()


class BusCreate(BusBase):
    pass


class BusUpdate(BaseModel):
    fleet_number: str | None = Field(default=None, max_length=50)
    bus_name: str | None = Field(default=None, min_length=2, max_length=150)
    bus_type: BusType | None = None
    service_type: ServiceType | None = None
    fuel_type: FuelType | None = None
    manufacturer: str | None = Field(default=None, max_length=100)
    model_name: str | None = Field(default=None, max_length=100)
    manufacturing_year: int | None = Field(default=None, ge=1980, le=2100)
    total_capacity: int | None = Field(default=None, ge=1, le=200)
    number_of_decks: int | None = Field(default=None, ge=1, le=2)
    has_air_conditioning: bool | None = None
    status: BusStatus | None = None
    is_active: bool | None = None

    @field_validator(
        "fleet_number",
        "bus_name",
        "manufacturer",
        "model_name",
        mode="before",
    )
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value


class BusStatusUpdate(BaseModel):
    status: BusStatus


class BusResponse(BusBase):
    id: int
    operator_id: int
    status: BusStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)