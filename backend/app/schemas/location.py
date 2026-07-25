from pydantic import BaseModel, ConfigDict, Field


class CountryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    code: str = Field(min_length=2, max_length=3)


class CountryResponse(BaseModel):
    id: int
    name: str
    code: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class StateCreate(BaseModel):
    country_id: int
    name: str = Field(min_length=2, max_length=100)
    code: str | None = Field(default=None, max_length=10)


class StateResponse(BaseModel):
    id: int
    country_id: int
    name: str
    code: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class DistrictCreate(BaseModel):
    state_id: int
    name: str = Field(min_length=2, max_length=120)


class DistrictResponse(BaseModel):
    id: int
    state_id: int
    name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class CityCreate(BaseModel):
    district_id: int
    name: str = Field(min_length=2, max_length=120)
    latitude: float | None = None
    longitude: float | None = None


class CityResponse(BaseModel):
    id: int
    district_id: int
    name: str
    latitude: float | None
    longitude: float | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class LocationAliasCreate(BaseModel):
    city_id: int
    alias: str = Field(min_length=2, max_length=150)


class LocationAliasResponse(BaseModel):
    id: int
    city_id: int
    alias: str

    model_config = ConfigDict(from_attributes=True)


class LocationPointCreate(BaseModel):
    city_id: int
    name: str = Field(min_length=2, max_length=150)
    address: str | None = Field(default=None, max_length=255)
    latitude: float | None = None
    longitude: float | None = None
    boarding_allowed: bool = True
    dropping_allowed: bool = True


class LocationPointResponse(BaseModel):
    id: int
    city_id: int
    name: str
    address: str | None
    latitude: float | None
    longitude: float | None
    boarding_allowed: bool
    dropping_allowed: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class LocationSearchResponse(BaseModel):
    city_id: int
    city_name: str
    district_name: str
    state_name: str
    country_name: str
    matched_value: str
    match_type: str