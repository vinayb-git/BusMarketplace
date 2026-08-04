from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.seat_layout_repository import (
    delete_seat,
    delete_template_seats,
    get_bus_by_id,
    get_operator_by_id,
    get_seat_by_id,
    get_template_by_code,
    get_template_by_id,
    list_templates,
    save_bus,
    save_template,
)
from app.schemas.seat_layout import (
    LayoutGeneratorType,
    SeatLayoutGenerateRequest,
    SeatLayoutTemplateCreate,
    SeatLayoutTemplateUpdate,
    SeatTemplateSeatCreate,
    SeatTemplateSeatUpdate,
)
from decimal import Decimal

from app.models.seat_layout import (
    SeatDeck,
    SeatLayoutTemplate,
    SeatLayoutTemplateSeat,
    SeatOrientation,
    SeatType,
)


def _normalize_code(value: str) -> str:
    return value.strip().upper().replace(" ", "_")


def _normalize_label(value: str) -> str:
    return value.strip().upper()


def _validate_seat_payloads(
    seats: list[SeatTemplateSeatCreate],
    max_rows: int,
    max_columns: int,
    number_of_decks: int,
) -> None:
    labels: set[str] = set()
    positions: set[tuple[str, int, int]] = set()

    for seat in seats:
        label = _normalize_label(seat.seat_label)

        if label in labels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate seat label: {label}",
            )

        labels.add(label)

        if seat.row_number > max_rows:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Seat {label} exceeds max_rows.",
            )

        if seat.column_number > max_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Seat {label} exceeds max_columns.",
            )

        if number_of_decks == 1 and seat.deck.value == "upper":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Seat {label} cannot be on upper deck "
                    "for a single-deck layout."
                ),
            )

        position = (
            seat.deck.value,
            seat.row_number,
            seat.column_number,
        )

        if position in positions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Duplicate seat position for seat {label}: "
                    f"{position}"
                ),
            )

        positions.add(position)


def get_templates(
    db: Session,
    operator_id: int | None = None,
):
    return list_templates(db, operator_id)


def get_template(
    db: Session,
    template_id: int,
):
    template = get_template_by_id(db, template_id)

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat layout template not found.",
        )

    return template


def create_template(
    db: Session,
    payload: SeatLayoutTemplateCreate,
):
    operator = get_operator_by_id(db, payload.operator_id)

    if not operator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator not found.",
        )

    normalized_code = _normalize_code(payload.code)

    if get_template_by_code(db, normalized_code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat layout template code already exists.",
        )

    _validate_seat_payloads(
        payload.seats,
        payload.max_rows,
        payload.max_columns,
        payload.number_of_decks,
    )

    template = SeatLayoutTemplate(
        operator_id=payload.operator_id,
        name=payload.name.strip(),
        code=normalized_code,
        description=(
            payload.description.strip()
            if payload.description
            else None
        ),
        number_of_decks=payload.number_of_decks,
        max_rows=payload.max_rows,
        max_columns=payload.max_columns,
        total_capacity=len(payload.seats),
        is_active=True,
    )

    template.seats = [
        SeatLayoutTemplateSeat(
            seat_label=_normalize_label(seat.seat_label),
            seat_type=seat.seat_type,
            deck=seat.deck,
            row_number=seat.row_number,
            column_number=seat.column_number,
            orientation=seat.orientation,
            is_window=seat.is_window,
            is_aisle=seat.is_aisle,
            is_last_row=seat.is_last_row,
            is_ladies_reserved=seat.is_ladies_reserved,
            fare_multiplier=seat.fare_multiplier,
            display_order=seat.display_order,
            is_active=seat.is_active,
        )
        for seat in payload.seats
    ]

    try:
        return save_template(db, template)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Template name or seat data already exists.",
        )


def update_template(
    db: Session,
    template_id: int,
    payload: SeatLayoutTemplateUpdate,
):
    template = get_template(db, template_id)
    update_data = payload.model_dump(exclude_unset=True)

    new_rows = update_data.get("max_rows", template.max_rows)
    new_columns = update_data.get(
        "max_columns",
        template.max_columns,
    )
    new_decks = update_data.get(
        "number_of_decks",
        template.number_of_decks,
    )

    for seat in template.seats:
        if seat.row_number > new_rows:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Seat {seat.seat_label} exceeds the new max_rows."
                ),
            )

        if seat.column_number > new_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Seat {seat.seat_label} exceeds "
                    "the new max_columns."
                ),
            )

        if new_decks == 1 and seat.deck.value == "upper":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Cannot change to one deck while upper-deck "
                    "seats exist."
                ),
            )

    for field, value in update_data.items():
        if field in {"name", "description"} and isinstance(value, str):
            value = value.strip()

        setattr(template, field, value)

    return save_template(db, template)


def add_template_seat(
    db: Session,
    template_id: int,
    payload: SeatTemplateSeatCreate,
):
    template = get_template(db, template_id)

    _validate_seat_payloads(
        [payload],
        template.max_rows,
        template.max_columns,
        template.number_of_decks,
    )

    normalized_label = _normalize_label(payload.seat_label)

    if any(
        seat.seat_label == normalized_label
        for seat in template.seats
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat label already exists in this template.",
        )

    if any(
        seat.deck == payload.deck
        and seat.row_number == payload.row_number
        and seat.column_number == payload.column_number
        for seat in template.seats
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat position already exists in this template.",
        )

    template.seats.append(
        SeatLayoutTemplateSeat(
            seat_label=normalized_label,
            seat_type=payload.seat_type,
            deck=payload.deck,
            row_number=payload.row_number,
            column_number=payload.column_number,
            orientation=payload.orientation,
            is_window=payload.is_window,
            is_aisle=payload.is_aisle,
            is_last_row=payload.is_last_row,
            is_ladies_reserved=payload.is_ladies_reserved,
            fare_multiplier=payload.fare_multiplier,
            display_order=payload.display_order,
            is_active=payload.is_active,
        )
    )

    template.total_capacity = len(template.seats)
    return save_template(db, template)


def update_template_seat(
    db: Session,
    template_id: int,
    seat_id: int,
    payload: SeatTemplateSeatUpdate,
):
    template = get_template(db, template_id)
    seat = get_seat_by_id(db, seat_id)

    if not seat or seat.layout_template_id != template.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found in this template.",
        )

    update_data = payload.model_dump(exclude_unset=True)

    new_label = _normalize_label(
        update_data.get("seat_label", seat.seat_label)
    )
    new_deck = update_data.get("deck", seat.deck)
    new_row = update_data.get("row_number", seat.row_number)
    new_column = update_data.get(
        "column_number",
        seat.column_number,
    )

    if new_row > template.max_rows:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seat exceeds max_rows.",
        )

    if new_column > template.max_columns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seat exceeds max_columns.",
        )

    if (
        template.number_of_decks == 1
        and new_deck.value == "upper"
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Upper-deck seat is not allowed.",
        )

    for existing in template.seats:
        if existing.id == seat.id:
            continue

        if existing.seat_label == new_label:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Seat label already exists.",
            )

        if (
            existing.deck == new_deck
            and existing.row_number == new_row
            and existing.column_number == new_column
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Seat position already exists.",
            )

    for field, value in update_data.items():
        if field == "seat_label" and value is not None:
            value = new_label

        setattr(seat, field, value)

    return save_template(db, template)


def remove_template_seat(
    db: Session,
    template_id: int,
    seat_id: int,
):
    template = get_template(db, template_id)
    seat = get_seat_by_id(db, seat_id)

    if not seat or seat.layout_template_id != template.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found in this template.",
        )

    delete_seat(db, seat)

    refreshed_template = get_template(db, template_id)
    refreshed_template.total_capacity = len(
        refreshed_template.seats
    )

    return save_template(db, refreshed_template)


def clone_template(
    db: Session,
    template_id: int,
    new_name: str,
    new_code: str,
):
    source = get_template(db, template_id)
    normalized_code = _normalize_code(new_code)

    if get_template_by_code(db, normalized_code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat layout template code already exists.",
        )

    cloned = SeatLayoutTemplate(
        operator_id=source.operator_id,
        name=new_name.strip(),
        code=normalized_code,
        description=source.description,
        number_of_decks=source.number_of_decks,
        max_rows=source.max_rows,
        max_columns=source.max_columns,
        total_capacity=source.total_capacity,
        is_active=True,
    )

    cloned.seats = [
        SeatLayoutTemplateSeat(
            seat_label=seat.seat_label,
            seat_type=seat.seat_type,
            deck=seat.deck,
            row_number=seat.row_number,
            column_number=seat.column_number,
            orientation=seat.orientation,
            is_window=seat.is_window,
            is_aisle=seat.is_aisle,
            is_last_row=seat.is_last_row,
            is_ladies_reserved=seat.is_ladies_reserved,
            fare_multiplier=seat.fare_multiplier,
            display_order=seat.display_order,
            is_active=seat.is_active,
        )
        for seat in source.seats
    ]

    return save_template(db, cloned)


def assign_template_to_bus(
    db: Session,
    bus_id: int,
    template_id: int,
):
    bus = get_bus_by_id(db, bus_id)

    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found.",
        )

    template = get_template(db, template_id)

    if template.operator_id != bus.operator_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "The template and bus must belong to "
                "the same operator."
            ),
        )

    if template.total_capacity != bus.total_capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": (
                    "Template capacity does not match bus capacity."
                ),
                "template_capacity": template.total_capacity,
                "bus_capacity": bus.total_capacity,
            },
        )

    bus.seat_layout_template_id = template.id
    save_bus(db, bus)

    return template

def generate_template_seats(
    db: Session,
    template_id: int,
    payload: SeatLayoutGenerateRequest,
):
    template = get_template(db, template_id)

    if template.seats and not payload.replace_existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "This template already contains seats. "
                "Set replace_existing=true to regenerate it."
            ),
        )

    if payload.rows > template.max_rows:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested rows exceed template max_rows.",
        )

    if payload.decks > template.number_of_decks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested decks exceed template number_of_decks.",
        )

    generated_seats: list[SeatLayoutTemplateSeat] = []

    if payload.layout_type == LayoutGeneratorType.SEATER_2X2:
        if template.max_columns < 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="2+2 seater requires at least 4 columns.",
            )

        for row in range(1, payload.rows + 1):
            row_letter = _row_label(row)

            for column in range(1, 5):
                generated_seats.append(
                    SeatLayoutTemplateSeat(
                        seat_label=f"{row_letter}{column}",
                        seat_type=SeatType.SEATER,
                        deck=SeatDeck.SINGLE,
                        row_number=row,
                        column_number=column,
                        orientation=SeatOrientation.FORWARD,
                        is_window=column in {1, 4},
                        is_aisle=column in {2, 3},
                        is_last_row=row == payload.rows,
                        is_ladies_reserved=False,
                        fare_multiplier=Decimal("1.00"),
                        display_order=len(generated_seats) + 1,
                        is_active=True,
                    )
                )

    elif payload.layout_type == LayoutGeneratorType.SEATER_2X1:
        if template.max_columns < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="2+1 seater requires at least 3 columns.",
            )

        for row in range(1, payload.rows + 1):
            row_letter = _row_label(row)

            for column in range(1, 4):
                generated_seats.append(
                    SeatLayoutTemplateSeat(
                        seat_label=f"{row_letter}{column}",
                        seat_type=SeatType.SEATER,
                        deck=SeatDeck.SINGLE,
                        row_number=row,
                        column_number=column,
                        orientation=SeatOrientation.FORWARD,
                        is_window=column in {1, 3},
                        is_aisle=column == 2,
                        is_last_row=row == payload.rows,
                        is_ladies_reserved=False,
                        fare_multiplier=Decimal("1.00"),
                        display_order=len(generated_seats) + 1,
                        is_active=True,
                    )
                )

    elif payload.layout_type == LayoutGeneratorType.SLEEPER_2X1:
        if template.max_columns < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="2+1 sleeper requires at least 3 columns.",
            )

        if payload.decks != 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="2+1 sleeper generation requires two decks.",
            )

        for deck in (SeatDeck.LOWER, SeatDeck.UPPER):
            prefix = "L" if deck == SeatDeck.LOWER else "U"

            for row in range(1, payload.rows + 1):
                for column in range(1, 4):
                    generated_seats.append(
                        SeatLayoutTemplateSeat(
                            seat_label=f"{prefix}{row}{column}",
                            seat_type=SeatType.SLEEPER,
                            deck=deck,
                            row_number=row,
                            column_number=column,
                            orientation=SeatOrientation.FORWARD,
                            is_window=column in {1, 3},
                            is_aisle=column == 2,
                            is_last_row=row == payload.rows,
                            is_ladies_reserved=False,
                            fare_multiplier=Decimal("1.00"),
                            display_order=len(generated_seats) + 1,
                            is_active=True,
                        )
                    )

    elif payload.layout_type == LayoutGeneratorType.MIXED_CUSTOM:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "mixed_custom layouts must be created or adjusted "
                "manually because seat labels and types vary."
            ),
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported layout generator type.",
        )

    if payload.replace_existing:
        delete_template_seats(db, template)

    template.seats.extend(generated_seats)
    template.total_capacity = len(generated_seats)

    return save_template(db, template)


def _row_label(row_number: int) -> str:
    label = ""
    number = row_number

    while number > 0:
        number, remainder = divmod(number - 1, 26)
        label = chr(65 + remainder) + label

    return label