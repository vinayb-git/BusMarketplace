from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.location import (
    City,
    Country,
    District,
    LocationAlias,
    LocationPoint,
    State,
)


def get_country_by_id(db: Session, country_id: int) -> Country | None:
    return db.get(Country, country_id)


def get_country_by_code(db: Session, code: str) -> Country | None:
    statement = select(Country).where(
        Country.code == code.upper().strip()
    )
    return db.scalar(statement)


def create_country(
    db: Session,
    *,
    name: str,
    code: str,
) -> Country:
    country = Country(
        name=name.strip(),
        code=code.upper().strip(),
    )

    db.add(country)
    db.commit()
    db.refresh(country)

    return country


def get_state_by_id(db: Session, state_id: int) -> State | None:
    return db.get(State, state_id)


def create_state(
    db: Session,
    *,
    country_id: int,
    name: str,
    code: str | None,
) -> State:
    state = State(
        country_id=country_id,
        name=name.strip(),
        code=code.upper().strip() if code else None,
    )

    db.add(state)
    db.commit()
    db.refresh(state)

    return state


def get_district_by_id(
    db: Session,
    district_id: int,
) -> District | None:
    return db.get(District, district_id)


def create_district(
    db: Session,
    *,
    state_id: int,
    name: str,
) -> District:
    district = District(
        state_id=state_id,
        name=name.strip(),
    )

    db.add(district)
    db.commit()
    db.refresh(district)

    return district


def get_city_by_id(db: Session, city_id: int) -> City | None:
    return db.get(City, city_id)


def create_city(
    db: Session,
    *,
    district_id: int,
    name: str,
    latitude: float | None,
    longitude: float | None,
) -> City:
    city = City(
        district_id=district_id,
        name=name.strip(),
        latitude=latitude,
        longitude=longitude,
    )

    db.add(city)
    db.commit()
    db.refresh(city)

    return city


def create_location_alias(
    db: Session,
    *,
    city_id: int,
    alias: str,
) -> LocationAlias:
    location_alias = LocationAlias(
        city_id=city_id,
        alias=alias.strip(),
    )

    db.add(location_alias)
    db.commit()
    db.refresh(location_alias)

    return location_alias


def create_location_point(
    db: Session,
    *,
    city_id: int,
    name: str,
    address: str | None,
    latitude: float | None,
    longitude: float | None,
    boarding_allowed: bool,
    dropping_allowed: bool,
) -> LocationPoint:
    point = LocationPoint(
        city_id=city_id,
        name=name.strip(),
        address=address.strip() if address else None,
        latitude=latitude,
        longitude=longitude,
        boarding_allowed=boarding_allowed,
        dropping_allowed=dropping_allowed,
    )

    db.add(point)
    db.commit()
    db.refresh(point)

    return point


def list_countries(db: Session) -> list[Country]:
    statement = (
        select(Country)
        .where(Country.is_active.is_(True))
        .order_by(Country.name)
    )

    return list(db.scalars(statement).all())


def list_states_by_country(
    db: Session,
    country_id: int,
) -> list[State]:
    statement = (
        select(State)
        .where(
            State.country_id == country_id,
            State.is_active.is_(True),
        )
        .order_by(State.name)
    )

    return list(db.scalars(statement).all())


def list_districts_by_state(
    db: Session,
    state_id: int,
) -> list[District]:
    statement = (
        select(District)
        .where(
            District.state_id == state_id,
            District.is_active.is_(True),
        )
        .order_by(District.name)
    )

    return list(db.scalars(statement).all())


def list_cities_by_district(
    db: Session,
    district_id: int,
) -> list[City]:
    statement = (
        select(City)
        .where(
            City.district_id == district_id,
            City.is_active.is_(True),
        )
        .order_by(City.name)
    )

    return list(db.scalars(statement).all())


def list_points_by_city(
    db: Session,
    city_id: int,
) -> list[LocationPoint]:
    statement = (
        select(LocationPoint)
        .where(
            LocationPoint.city_id == city_id,
            LocationPoint.is_active.is_(True),
        )
        .order_by(LocationPoint.name)
    )

    return list(db.scalars(statement).all())


def search_locations(
    db: Session,
    query: str,
) -> list[tuple[City, District, State, Country, str, str]]:
    search_value = f"%{query.strip()}%"

    city_statement = (
        select(City, District, State, Country)
        .join(District, City.district_id == District.id)
        .join(State, District.state_id == State.id)
        .join(Country, State.country_id == Country.id)
        .where(
            City.is_active.is_(True),
            City.name.ilike(search_value),
        )
        .limit(20)
    )

    results: list[
        tuple[City, District, State, Country, str, str]
    ] = []

    for city, district, state, country in db.execute(city_statement):
        results.append(
            (
                city,
                district,
                state,
                country,
                city.name,
                "city",
            )
        )

    alias_statement = (
        select(
            LocationAlias,
            City,
            District,
            State,
            Country,
        )
        .join(City, LocationAlias.city_id == City.id)
        .join(District, City.district_id == District.id)
        .join(State, District.state_id == State.id)
        .join(Country, State.country_id == Country.id)
        .where(
            City.is_active.is_(True),
            LocationAlias.alias.ilike(search_value),
        )
        .limit(20)
    )

    for alias, city, district, state, country in db.execute(
        alias_statement
    ):
        results.append(
            (
                city,
                district,
                state,
                country,
                alias.alias,
                "alias",
            )
        )

    return results[:20]