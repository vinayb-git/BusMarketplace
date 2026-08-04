from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.seat_layout import (
    SeatDeck,
    SeatOrientation,
    SeatType,
)
import enum


class SeatTemplateSeatCreate(BaseModel):
    seat_label: str = Field(min_length=1, max_length=20)
    seat_type: SeatType
    deck: SeatDeck = SeatDeck.SINGLE
    row_number: int = Field(ge=1)
    column_number: int = Field(ge=1)
    orientation: SeatOrientation = SeatOrientation.FORWARD
    is_window: bool = False
    is_aisle: bool = False
    is_last_row: bool = False
    is_ladies_reserved: bool = False
    fare_multiplier: Decimal = Field(
        default=Decimal("1.00"),
        gt=0,
        max_digits=5,
        decimal_places=2,
    )
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True


class SeatTemplateSeatUpdate(BaseModel):
    seat_label: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )
    seat_type: SeatType | None = None
    deck: SeatDeck | None = None
    row_number: int | None = Field(default=None, ge=1)
    column_number: int | None = Field(default=None, ge=1)
    orientation: SeatOrientation | None = None
    is_window: bool | None = None
    is_aisle: bool | None = None
    is_last_row: bool | None = None
    is_ladies_reserved: bool | None = None
    fare_multiplier: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=5,
        decimal_places=2,
    )
    display_order: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class SeatTemplateSeatResponse(BaseModel):
    id: int
    layout_template_id: int
    seat_label: str
    seat_type: SeatType
    deck: SeatDeck
    row_number: int
    column_number: int
    orientation: SeatOrientation
    is_window: bool
    is_aisle: bool
    is_last_row: bool
    is_ladies_reserved: bool
    fare_multiplier: Decimal
    display_order: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class SeatLayoutTemplateCreate(BaseModel):
    operator_id: int
    name: str = Field(min_length=2, max_length=150)
    code: str = Field(min_length=2, max_length=75)
    description: str | None = None
    number_of_decks: int = Field(default=1, ge=1, le=2)
    max_rows: int = Field(ge=1)
    max_columns: int = Field(ge=1)
    seats: list[SeatTemplateSeatCreate] = Field(default_factory=list)


class SeatLayoutTemplateUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    description: str | None = None
    number_of_decks: int | None = Field(default=None, ge=1, le=2)
    max_rows: int | None = Field(default=None, ge=1)
    max_columns: int | None = Field(default=None, ge=1)
    is_active: bool | None = None


class SeatLayoutTemplateResponse(BaseModel):
    id: int
    operator_id: int
    name: str
    code: str
    description: str | None
    number_of_decks: int
    max_rows: int
    max_columns: int
    total_capacity: int
    is_active: bool
    seats: list[SeatTemplateSeatResponse]

    model_config = ConfigDict(from_attributes=True)


class BusLayoutAssignment(BaseModel):
    seat_layout_template_id: int


class CloneSeatLayoutTemplate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150,
    )
    code: str = Field(
        min_length=2,
        max_length=75,
    )
    
class LayoutGeneratorType(str, enum.Enum):
    SEATER_2X2 = "2+2_seater"
    SEATER_2X1 = "2+1_seater"
    SLEEPER_2X1 = "2+1_sleeper"
    MIXED_CUSTOM = "mixed_custom"


class SeatLayoutGenerateRequest(BaseModel):
    layout_type: LayoutGeneratorType
    rows: int = Field(ge=1, le=30)
    decks: int = Field(default=1, ge=1, le=2)
    replace_existing: bool = False