from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.seat_layout import (
    BusLayoutAssignment,
    CloneSeatLayoutTemplate,
    SeatLayoutGenerateRequest,
    SeatLayoutTemplateCreate,
    SeatLayoutTemplateResponse,
    SeatLayoutTemplateUpdate,
    SeatTemplateSeatCreate,
    SeatTemplateSeatUpdate,
)
from app.services.seat_layout_service import (
    add_template_seat,
    assign_template_to_bus,
    clone_template,
    create_template,
    generate_template_seats,
    get_template,
    get_templates,
    remove_template_seat,
    update_template,
    update_template_seat,
)

router = APIRouter(
    prefix="/seat-layouts",
    tags=["Seat Layout"],
)

@router.get(
    "",
    response_model=list[SeatLayoutTemplateResponse],
)
def list_templates_endpoint(
    operator_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return get_templates(db, operator_id)

@router.get(
    "/{template_id}",
    response_model=SeatLayoutTemplateResponse,
)
def get_template_endpoint(
    template_id: int,
    db: Session = Depends(get_db),
):
    return get_template(db, template_id)
@router.post(
    "",
    response_model=SeatLayoutTemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_template_endpoint(
    payload: SeatLayoutTemplateCreate,
    db: Session = Depends(get_db),
):
    return create_template(db, payload)
@router.put(
    "/{template_id}",
    response_model=SeatLayoutTemplateResponse,
)
def update_template_endpoint(
    template_id: int,
    payload: SeatLayoutTemplateUpdate,
    db: Session = Depends(get_db),
):
    return update_template(
        db,
        template_id,
        payload,
    )
@router.post(
    "/{template_id}/seats",
    response_model=SeatLayoutTemplateResponse,
)
def add_seat_endpoint(
    template_id: int,
    payload: SeatTemplateSeatCreate,
    db: Session = Depends(get_db),
):
    return add_template_seat(
        db,
        template_id,
        payload,
    )
@router.put(
    "/{template_id}/seats/{seat_id}",
    response_model=SeatLayoutTemplateResponse,
)
def update_seat_endpoint(
    template_id: int,
    seat_id: int,
    payload: SeatTemplateSeatUpdate,
    db: Session = Depends(get_db),
):
    return update_template_seat(
        db,
        template_id,
        seat_id,
        payload,
    )
@router.delete(
    "/{template_id}/seats/{seat_id}",
    response_model=SeatLayoutTemplateResponse,
)
def delete_seat_endpoint(
    template_id: int,
    seat_id: int,
    db: Session = Depends(get_db),
):
    return remove_template_seat(
        db,
        template_id,
        seat_id,
    )
@router.post(
    "/{template_id}/clone",
    response_model=SeatLayoutTemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
def clone_template_endpoint(
    template_id: int,
    payload: CloneSeatLayoutTemplate,
    db: Session = Depends(get_db),
):
    return clone_template(
        db,
        template_id,
        payload.name,
        payload.code,
    )
@router.put(
    "/bus/{bus_id}",
    response_model=SeatLayoutTemplateResponse,
)
def assign_template_endpoint(
    bus_id: int,
    payload: BusLayoutAssignment,
    db: Session = Depends(get_db),
):
    return assign_template_to_bus(
        db,
        bus_id,
        payload.seat_layout_template_id,
    )
@router.post(
    "/{template_id}/generate",
    response_model=SeatLayoutTemplateResponse,
)
def generate_template_seats_endpoint(
    template_id: int,
    payload: SeatLayoutGenerateRequest,
    db: Session = Depends(get_db),
):
    return generate_template_seats(
        db,
        template_id,
        payload,
    )