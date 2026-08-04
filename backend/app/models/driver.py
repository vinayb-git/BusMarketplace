from __future__ import annotations

import enum
from datetime import date, datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.models.bus import Bus
    from app.models.operator import Operator


class DriverStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class Driver(Base):
    __tablename__ = "drivers"

    __table_args__ = (
        UniqueConstraint(
            "operator_id",
            "license_number",
            name="uq_driver_operator_license",
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

    assigned_bus_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "buses.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    employee_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    alternate_phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    blood_group: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    emergency_contact_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    emergency_contact_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    license_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    license_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    license_issue_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    license_expiry_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    government_id_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    government_id_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    years_of_experience: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    status: Mapped[DriverStatus] = mapped_column(
        Enum(
            DriverStatus,
            name="driver_status_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
        default=DriverStatus.ACTIVE,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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
        back_populates="drivers",
    )

    assigned_bus: Mapped["Bus | None"] = relationship(
        "Bus",
        back_populates="drivers",
    )