from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..db.base import get_db
from ..schemas.event import EventCreate, EventRead, EventUpdate
from ..services.event_service import EventService

router = APIRouter()


@router.post(
    "/events",
    response_model=EventRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create Event",
    description="Create a new event with title, time range, and optional details.",
    responses={
        201: {"description": "Event created successfully"},
        400: {"description": "Validation error"},
    },
)
def create_event(payload: EventCreate, db: Session = Depends(get_db)) -> EventRead:
    """
    Create a new event.

    Parameters:
        payload: EventCreate - Required event details.
    Returns:
        EventRead: The created event.
    """
    service = EventService(db)
    try:
        event = service.create_event(
            title=payload.title,
            description=payload.description,
            location=payload.location,
            start_time=payload.start_time,
            end_time=payload.end_time,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return EventRead.model_validate(event)


@router.get(
    "/events/{event_id}",
    response_model=EventRead,
    summary="Get Event",
    description="Retrieve an event by its ID, including its attendees.",
    responses={
        200: {"description": "Event retrieved successfully"},
        404: {"description": "Event not found"},
    },
)
def get_event(event_id: int, db: Session = Depends(get_db)) -> EventRead:
    """
    Get an event by ID including attendees.
    """
    service = EventService(db)
    event = service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventRead.model_validate(event)


@router.get(
    "/events",
    response_model=list[EventRead],
    summary="List Events",
    description="List events with pagination and optional search by title.",
    responses={200: {"description": "List of events"}},
)
def list_events(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of items to return"),
    search: Optional[str] = Query(None, description="Search term for event title"),
    db: Session = Depends(get_db),
) -> List[EventRead]:
    """
    List events with optional pagination and search.
    """
    service = EventService(db)
    events, _ = service.list_events(skip=skip, limit=limit, search=search)
    return [EventRead.model_validate(e) for e in events]


@router.patch(
    "/events/{event_id}",
    response_model=EventRead,
    summary="Update Event",
    description="Update fields of an existing event.",
    responses={
        200: {"description": "Event updated successfully"},
        400: {"description": "Validation error"},
        404: {"description": "Event not found"},
    },
)
def update_event(event_id: int, payload: EventUpdate, db: Session = Depends(get_db)) -> EventRead:
    """
    Update an event by ID.
    """
    service = EventService(db)
    data = payload.model_dump(exclude_unset=True)
    try:
        event = service.update_event(event_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventRead.model_validate(event)


@router.delete(
    "/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Event",
    description="Delete an event by its ID. Attendees are deleted as well.",
    responses={204: {"description": "Event deleted"}, 404: {"description": "Event not found"}},
)
def delete_event(event_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete an event by ID. Returns no content on success.
    """
    service = EventService(db)
    ok = service.delete_event(event_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Event not found")
    return None
