from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..db.base import get_db
from ..schemas.attendee import AttendeeCreate, AttendeeRead, AttendeeUpdate
from ..services.attendee_service import AttendeeService

router = APIRouter()


@router.post(
    "/attendees",
    response_model=AttendeeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create Attendee",
    description="Create a new attendee under a specific event.",
    responses={
        201: {"description": "Attendee created successfully"},
        400: {"description": "Validation error or event not found"},
    },
)
def create_attendee(payload: AttendeeCreate, db: Session = Depends(get_db)) -> AttendeeRead:
    """
    Create a new attendee.

    Parameters:
        payload: AttendeeCreate - Required attendee details with event_id.
    Returns:
        AttendeeRead: The created attendee.
    """
    service = AttendeeService(db)
    try:
        attendee = service.create_attendee(event_id=payload.event_id, name=payload.name, email=payload.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return AttendeeRead.model_validate(attendee)


@router.get(
    "/attendees/{attendee_id}",
    response_model=AttendeeRead,
    summary="Get Attendee",
    description="Retrieve an attendee by its ID.",
    responses={
        200: {"description": "Attendee retrieved successfully"},
        404: {"description": "Attendee not found"},
    },
)
def get_attendee(attendee_id: int, db: Session = Depends(get_db)) -> AttendeeRead:
    """
    Get an attendee by ID.
    """
    service = AttendeeService(db)
    attendee = service.get_attendee(attendee_id)
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return AttendeeRead.model_validate(attendee)


@router.get(
    "/attendees",
    response_model=list[AttendeeRead],
    summary="List Attendees",
    description="List attendees with pagination. Optionally filter by event_id and search by name.",
    responses={200: {"description": "List of attendees"}},
)
def list_attendees(
    event_id: Optional[int] = Query(None, description="Filter by event ID"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of items to return"),
    search: Optional[str] = Query(None, description="Search term for attendee name"),
    db: Session = Depends(get_db),
) -> List[AttendeeRead]:
    """
    List attendees with optional pagination, filter, and search.
    """
    service = AttendeeService(db)
    attendees, _ = service.list_attendees(event_id=event_id, skip=skip, limit=limit, search=search)
    return [AttendeeRead.model_validate(a) for a in attendees]


@router.patch(
    "/attendees/{attendee_id}",
    response_model=AttendeeRead,
    summary="Update Attendee",
    description="Update fields of an existing attendee.",
    responses={
        200: {"description": "Attendee updated successfully"},
        404: {"description": "Attendee not found"},
    },
)
def update_attendee(attendee_id: int, payload: AttendeeUpdate, db: Session = Depends(get_db)) -> AttendeeRead:
    """
    Update an attendee by ID.
    """
    service = AttendeeService(db)
    data = payload.model_dump(exclude_unset=True)
    attendee = service.update_attendee(attendee_id, data)
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return AttendeeRead.model_validate(attendee)


@router.delete(
    "/attendees/{attendee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Attendee",
    description="Delete an attendee by its ID.",
    responses={204: {"description": "Attendee deleted"}, 404: {"description": "Attendee not found"}},
)
def delete_attendee(attendee_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete an attendee by ID. Returns no content on success.
    """
    service = AttendeeService(db)
    ok = service.delete_attendee(attendee_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return None
