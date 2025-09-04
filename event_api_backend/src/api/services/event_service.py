from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from ..models.event import Event
from ..repositories.event_repository import EventRepository


class EventService:
    """
    Service layer for business logic related to events.
    """

    def __init__(self, db: Session) -> None:
        self.repo = EventRepository(db)

    # PUBLIC_INTERFACE
    def create_event(self, *, title: str, description: Optional[str], location: Optional[str], start_time, end_time) -> Event:
        """
        Create a new event.

        Args:
            title: Event title.
            description: Optional description.
            location: Optional location.
            start_time: Start datetime.
            end_time: End datetime.

        Returns:
            Persisted Event model.
        """
        # Additional guard (schemas validate already)
        if end_time <= start_time:
            raise ValueError("end_time must be after start_time")

        event = Event(
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
        )
        return self.repo.create(event)

    # PUBLIC_INTERFACE
    def get_event(self, event_id: int) -> Optional[Event]:
        """
        Retrieve event by ID including attendees list.
        """
        return self.repo.get(event_id)

    # PUBLIC_INTERFACE
    def list_events(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> Tuple[List[Event], int]:
        """
        List events with pagination and optional search by title.
        """
        return self.repo.list(skip=skip, limit=limit, search=search)

    # PUBLIC_INTERFACE
    def update_event(self, event_id: int, data: dict) -> Optional[Event]:
        """
        Update an event by ID with partial data.
        """
        # If both times present, validate order
        if "start_time" in data and "end_time" in data:
            st = data["start_time"]
            et = data["end_time"]
            if st is not None and et is not None and et <= st:
                raise ValueError("end_time must be after start_time")
        return self.repo.update(event_id, data)

    # PUBLIC_INTERFACE
    def delete_event(self, event_id: int) -> bool:
        """
        Delete event by ID.
        """
        return self.repo.delete(event_id)
