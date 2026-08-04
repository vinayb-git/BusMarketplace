from __future__ import annotations

import enum
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.models.bus import Bus
    from app.models.operator import Operator


class SeatType(str, enum.Enum):
    SEATER = "seater"
    SEMI_SLEEPER = "semi_sleeper"
    SLEEPER = "sleeper"


class SeatDeck(str, enum.Enum):
    SINGLE = "single"
    LOWER = "lower"
    UPPER = "upper"


class SeatOrientation(str, enum.Enum):
    FORWARD = "forward"
    REARWARD = "rearward"
    SIDEWAYS = "sideways"


class SeatLayoutTemplate(Base):
    __tablename__ = "seat_layout_templates"

    __table_args__ = (
        UniqueConstraint(
            "operator_id",
            "name",
            name="uq_seat_layout_operator_name",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    operator_id: Mapped[int] = mapped_column(
        ForeignKey(
            "operators.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(75),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    number_of_decks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    max_rows: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    max_columns: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    total_capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    operator: Mapped["Operator"] = relationship(
        "Operator",
    )

    seats: Mapped[list["SeatLayoutTemplateSeat"]] = relationship(
        "SeatLayoutTemplateSeat",
        back_populates="layout_template",
        cascade="all, delete-orphan",
        order_by="SeatLayoutTemplateSeat.display_order",
    )

    buses: Mapped[list["Bus"]] = relationship(
        "Bus",
        back_populates="seat_layout_template",
    )


class SeatLayoutTemplateSeat(Base):
    __tablename__ = "seat_layout_template_seats"

    __table_args__ = (
        UniqueConstraint(
            "layout_template_id",
            "seat_label",
            name="uq_layout_template_seat_label",
        ),
        UniqueConstraint(
            "layout_template_id",
            "deck",
            "row_number",
            "column_number",
            name="uq_layout_template_seat_position",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    layout_template_id: Mapped[int] = mapped_column(
        ForeignKey(
            "seat_layout_templates.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Operator-defined label:
    # L1, C1, C2, U1, A1, B1, etc.
    seat_label: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    seat_type: Mapped[SeatType] = mapped_column(
        Enum(
            SeatType,
            name="seat_type_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
    )

    deck: Mapped[SeatDeck] = mapped_column(
        Enum(
            SeatDeck,
            name="seat_deck_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
        default=SeatDeck.SINGLE,
    )

    row_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    column_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    orientation: Mapped[SeatOrientation] = mapped_column(
        Enum(
            SeatOrientation,
            name="seat_orientation_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
        default=SeatOrientation.FORWARD,
    )

    is_window: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_aisle: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_last_row: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_ladies_reserved: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    fare_multiplier: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("1.00"),
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    layout_template: Mapped["SeatLayoutTemplate"] = relationship(
        "SeatLayoutTemplate",
        back_populates="seats",
    )