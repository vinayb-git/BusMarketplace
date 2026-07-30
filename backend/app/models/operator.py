from __future__ import annotations

from typing import TYPE_CHECKING
import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
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

class OperatorStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    owner_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
        index=True,
    )

    legal_name: Mapped[str] = mapped_column(String(200), nullable=False)
    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    registration_number: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )

    tax_id: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
    )

    address_line_1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line_2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)

    status: Mapped[OperatorStatus] = mapped_column(
        Enum(OperatorStatus, name="operator_status"),
        default=OperatorStatus.PENDING,
        nullable=False,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    owner = relationship("User")
    city = relationship("City")

    contacts: Mapped[list["OperatorContact"]] = relationship(
        back_populates="operator",
        cascade="all, delete-orphan",
    )

    bank_accounts: Mapped[list["OperatorBankAccount"]] = relationship(
        back_populates="operator",
        cascade="all, delete-orphan",
    )

    buses: Mapped[list["Bus"]] = relationship(
    back_populates="operator",
    cascade="all, delete-orphan",
    )


class OperatorContact(Base):
    __tablename__ = "operator_contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    operator_id: Mapped[int] = mapped_column(
        ForeignKey("operators.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    job_title: Mapped[str | None] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    operator: Mapped["Operator"] = relationship(
        back_populates="contacts",
    )


class OperatorBankAccount(Base):
    __tablename__ = "operator_bank_accounts"

    __table_args__ = (
        UniqueConstraint(
            "operator_id",
            "account_number",
            name="uq_operator_bank_account",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    operator_id: Mapped[int] = mapped_column(
        ForeignKey("operators.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    account_name: Mapped[str] = mapped_column(String(150), nullable=False)
    account_number: Mapped[str] = mapped_column(String(100), nullable=False)
    bank_name: Mapped[str] = mapped_column(String(150), nullable=False)
    routing_code: Mapped[str] = mapped_column(String(50), nullable=False)
    account_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    operator: Mapped["Operator"] = relationship(
        back_populates="bank_accounts",
    )