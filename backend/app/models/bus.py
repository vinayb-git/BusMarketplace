from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING

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

if TYPE_CHECKING:
    from app.models.fleet_master import (
        BusClassMaster,
        BusConfigurationMaster,
        BusTypeMaster,
        FuelTypeMaster,
        ServiceCategoryMaster,
    )
    from app.models.operator import Operator
    from app.models.fleet_master import (
    AmenityMaster,
    BusClassMaster,
    BusConfigurationMaster,
    BusTypeMaster,
    FuelTypeMaster,
    ServiceCategoryMaster,
    )
    from app.models.seat_layout import SeatLayoutTemplate


# =========================================================
# Legacy enums
# =========================================================
# Keep these temporarily because the current schemas,
# repositories, services, and APIs still depend on them.
# We will remove them after the master-data migration
# and API refactor are completed.


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


# BusStatus remains an enum because it represents
# a controlled system workflow rather than master data.
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

    # =====================================================
    # Existing legacy classification fields
    # =====================================================
    # These fields remain temporarily so existing APIs
    # continue functioning during the migration.

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

    # =====================================================
    # New master-data foreign keys
    # =====================================================
    # These are nullable during the transition because
    # existing buses do not yet have master-table IDs.
    #
    # After we seed and backfill the data, we will change
    # the required columns to nullable=False.

    bus_type_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "bus_types.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    configuration_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "bus_configurations.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    fuel_type_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "fuel_types.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    service_category_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "service_categories.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    bus_class_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "bus_classes.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    seat_layout_template_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "seat_layout_templates.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    # =====================================================
    # Vehicle information
    # =====================================================

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

    # =====================================================
    # Operational status
    # =====================================================

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

    # =====================================================
    # Relationships
    # =====================================================

    operator: Mapped["Operator"] = relationship(
        "Operator",
        back_populates="buses",
    )

    bus_type_master: Mapped["BusTypeMaster | None"] = relationship(
        "BusTypeMaster",
        back_populates="buses",
        foreign_keys=[bus_type_id],
    )

    configuration_master: Mapped[
        "BusConfigurationMaster | None"
    ] = relationship(
        "BusConfigurationMaster",
        back_populates="buses",
        foreign_keys=[configuration_id],
    )

    fuel_type_master: Mapped["FuelTypeMaster | None"] = relationship(
        "FuelTypeMaster",
        back_populates="buses",
        foreign_keys=[fuel_type_id],
    )

    service_category_master: Mapped[
        "ServiceCategoryMaster | None"
    ] = relationship(
        "ServiceCategoryMaster",
        back_populates="buses",
        foreign_keys=[service_category_id],
    )

    bus_class_master: Mapped["BusClassMaster | None"] = relationship(
        "BusClassMaster",
        back_populates="buses",
        foreign_keys=[bus_class_id],
    )

    amenities: Mapped[list["AmenityMaster"]] = relationship(
        "AmenityMaster",
        secondary="bus_amenities",
        back_populates="buses",
    )
    seat_layout_template: Mapped["SeatLayoutTemplate | None"] = relationship(
        "SeatLayoutTemplate",
        back_populates="buses",
    )
    drivers: Mapped[list["Driver"]] = relationship(
    "Driver",
    back_populates="assigned_bus",
    )