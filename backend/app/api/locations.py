from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.database.session import get_db
from app.models.user import User
from app.repositories.location_repository import (
    create_city,
    create_country,
    create_district,
    create_location_alias,
    create_location_point,
    create_state,
    get_city_by_id,
    get_country_by_code,
    get_country_by_id,
    get_district_by_id,
    get_state_by_id,
    list_cities_by_district,
    list_countries,
    list_districts_by_state,
    list_points_by_city,
    list_states_by_country,
    search_locations,
)
from app.schemas.location import (
    CityCreate,
    CityResponse,
    CountryCreate,
    CountryResponse,
    DistrictCreate,
    DistrictResponse,
    LocationAliasCreate,
    LocationAliasResponse,
    LocationPointCreate,
    LocationPointResponse,
    LocationSearchResponse,
    StateCreate,
    StateResponse,
)


router = APIRouter(
    prefix="/locations",
    tags=["Locations"],
)


@router.get(
    "/countries",
    response_model=list[CountryResponse],
)
def get_countries(
    db: Session = Depends(get_db),
):
    return list_countries(db)


@router.get(
    "/countries/{country_id}/states",
    response_model=list[StateResponse],
)
def get_states(
    country_id: int,
    db: Session = Depends(get_db),
):
    return list_states_by_country(db, country_id)


@router.get(
    "/states/{state_id}/districts",
    response_model=list[DistrictResponse],
)
def get_districts(
    state_id: int,
    db: Session = Depends(get_db),
):
    return list_districts_by_state(db, state_id)


@router.get(
    "/districts/{district_id}/cities",
    response_model=list[CityResponse],
)
def get_cities(
    district_id: int,
    db: Session = Depends(get_db),
):
    return list_cities_by_district(db, district_id)


@router.get(
    "/cities/{city_id}/points",
    response_model=list[LocationPointResponse],
)
def get_city_points(
    city_id: int,
    db: Session = Depends(get_db),
):
    return list_points_by_city(db, city_id)


@router.get(
    "/search",
    response_model=list[LocationSearchResponse],
)
def search(
    q: str = Query(min_length=2, max_length=100),
    db: Session = Depends(get_db),
):
    results = search_locations(db, q)

    return [
        LocationSearchResponse(
            city_id=city.id,
            city_name=city.name,
            district_name=district.name,
            state_name=state.name,
            country_name=country.name,
            matched_value=matched_value,
            match_type=match_type,
        )
        for (
            city,
            district,
            state,
            country,
            matched_value,
            match_type,
        ) in results
    ]


@router.post(
    "/countries",
    response_model=CountryResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_country(
    request: CountryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    if get_country_by_code(db, request.code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A country with this code already exists.",
        )

    return create_country(
        db,
        name=request.name,
        code=request.code,
    )


@router.post(
    "/states",
    response_model=StateResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_state(
    request: StateCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    if not get_country_by_id(db, request.country_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found.",
        )

    return create_state(
        db,
        country_id=request.country_id,
        name=request.name,
        code=request.code,
    )


@router.post(
    "/districts",
    response_model=DistrictResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_district(
    request: DistrictCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    if not get_state_by_id(db, request.state_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="State not found.",
        )

    return create_district(
        db,
        state_id=request.state_id,
        name=request.name,
    )


@router.post(
    "/cities",
    response_model=CityResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_city(
    request: CityCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    if not get_district_by_id(db, request.district_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found.",
        )

    return create_city(
        db,
        district_id=request.district_id,
        name=request.name,
        latitude=request.latitude,
        longitude=request.longitude,
    )


@router.post(
    "/aliases",
    response_model=LocationAliasResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_alias(
    request: LocationAliasCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    if not get_city_by_id(db, request.city_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found.",
        )

    return create_location_alias(
        db,
        city_id=request.city_id,
        alias=request.alias,
    )


@router.post(
    "/points",
    response_model=LocationPointResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_location_point(
    request: LocationPointCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    if not get_city_by_id(db, request.city_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found.",
        )

    return create_location_point(
        db,
        city_id=request.city_id,
        name=request.name,
        address=request.address,
        latitude=request.latitude,
        longitude=request.longitude,
        boarding_allowed=request.boarding_allowed,
        dropping_allowed=request.dropping_allowed,
    )