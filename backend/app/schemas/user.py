from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class UserCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, min_length=7, max_length=20)
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)