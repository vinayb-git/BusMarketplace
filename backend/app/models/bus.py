import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class BusType(str, enum.Enum):
    SEATER = "seater"
    SLEEPER = "sleeper"
    SEMI_SLEEPER = "semi_sleeper"
    SEATER_SLEEPER = "seater_sleeper"


class ServiceType(str, enum.Enum):
    ORDINARY = "ordinary"
    EXPRESS = "express"
    DELUXE = "deluxe"
    LUXURY = "luxury"
    PREMIUM = "premium"


class FuelType(str, enum.Enum):
    DIESEL = "diesel"
    PETROL = "petrol"
    CNG = "cng"
    ELECTRIC = "electric"
    HYBRID = "hybrid"


class BusStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"


class Bus(Base):
    __tablename__ = "buses"
    __table_args__ = (
        UniqueConstraint(
            "operator_id",
            "fleet_number",
            name="uq_bus_operator_fleet_number",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    operator_id: Mapped[int] = mapped_column(
        ForeignKey("operators.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    registration_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    fleet_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )

    bus_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    bus_type: Mapped[BusType] = mapped_column(
        Enum(
            BusType,
            name="bus_type_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
    )

    service_type: Mapped[ServiceType] = mapped_column(
        Enum(
            ServiceType,
            name="service_type_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
    )

    fuel_type: Mapped[FuelType] = mapped_column(
        Enum(
            FuelType,
            name="fuel_type_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
        default=FuelType.DIESEL,
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    model_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    manufacturing_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    total_capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    number_of_decks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    has_air_conditioning: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    status: Mapped[BusStatus] = mapped_column(
        Enum(
            BusStatus,
            name="bus_status_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
        default=BusStatus.ACTIVE,
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

    operator = relationship(
        "Operator",
        back_populates="buses",
    )