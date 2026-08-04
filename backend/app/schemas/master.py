from pydantic import BaseModel, ConfigDict, Field


class MasterDataResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str | None = None
    display_order: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class AmenityCreate(BaseModel):
    code: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = True


class AmenityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    display_order: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class BusAmenityAssignment(BaseModel):
    amenity_ids: list[int] = Field(min_length=1)