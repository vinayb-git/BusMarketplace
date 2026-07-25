from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.operator import OperatorStatus


class OperatorCreate(BaseModel):
    legal_name: str = Field(min_length=2, max_length=200)
    display_name: str = Field(min_length=2, max_length=150)
    registration_number: str | None = Field(default=None, max_length=100)
    tax_id: str | None = Field(default=None, max_length=50)
    address_line_1: str = Field(min_length=3, max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)
    city_id: int
    postal_code: str = Field(min_length=3, max_length=20)


class OperatorUpdate(BaseModel):
    legal_name: str | None = Field(default=None, min_length=2, max_length=200)
    display_name: str | None = Field(default=None, min_length=2, max_length=150)
    registration_number: str | None = Field(default=None, max_length=100)
    tax_id: str | None = Field(default=None, max_length=50)
    address_line_1: str | None = Field(default=None, min_length=3, max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)
    city_id: int | None = None
    postal_code: str | None = Field(default=None, min_length=3, max_length=20)


class OperatorContactCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    job_title: str | None = Field(default=None, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)
    is_primary: bool = False


class OperatorContactResponse(BaseModel):
    id: int
    operator_id: int
    full_name: str
    job_title: str | None
    email: EmailStr
    phone: str
    is_primary: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class OperatorBankAccountCreate(BaseModel):
    account_name: str = Field(min_length=2, max_length=150)
    account_number: str = Field(min_length=4, max_length=100)
    bank_name: str = Field(min_length=2, max_length=150)
    routing_code: str = Field(min_length=2, max_length=50)
    account_type: str | None = Field(default=None, max_length=50)
    is_primary: bool = False


class OperatorBankAccountResponse(BaseModel):
    id: int
    operator_id: int
    account_name: str
    account_number: str
    bank_name: str
    routing_code: str
    account_type: str | None
    is_primary: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class OperatorResponse(BaseModel):
    id: int
    owner_user_id: int
    legal_name: str
    display_name: str
    registration_number: str | None
    tax_id: str | None
    address_line_1: str
    address_line_2: str | None
    city_id: int
    postal_code: str
    status: OperatorStatus
    rejection_reason: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OperatorDetailResponse(OperatorResponse):
    contacts: list[OperatorContactResponse] = []
    bank_accounts: list[OperatorBankAccountResponse] = []


class OperatorRejectRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=1000)