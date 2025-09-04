from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from ..models.attendee import Attendee
from ..repositories.attendee_repository import AttendeeRepository
from ..repositories.event_repository import EventRepository


class AttendeeService:
    """
    Service layer for business logic related to attendees.
    """

    def __init__(self, db: Session) -> None:
        self.repo = AttendeeRepository(db)
        self.event_repo = EventRepository(db)

    # PUBLIC_INTERFACE
    def create_attendee(self, *, event_id: int, name: str, email: str) -> Attendee:
        """
        Create a new attendee under a specific event.

        Args:
            event_id: Event ID.
            name: Attendee name.
            email: Attendee email.

        Returns:
            Persisted Attendee model.

        Raises:
            ValueError: If the referenced event does not exist.
        """
        if not self.event_repo.get(event_id):
            raise ValueError(f"Event with id {event_id} not found")
        attendee = Attendee(event_id=event_id, name=name, email=email)
        return self.repo.create(attendee)

    # PUBLIC_INTERFACE
    def get_attendee(self, attendee_id: int) -> Optional[Attendee]:
        """
        Retrieve attendee by ID.
        """
        return self.repo.get(attendee_id)

    # PUBLIC_INTERFACE
    def list_attendees(self, event_id: Optional[int] = None, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> Tuple[List[Attendee], int]:
        """
        List attendees with pagination, optional filter by event_id and search by name.
        """
        return self.repo.list(event_id=event_id, skip=skip, limit=limit, search=search)

    # PUBLIC_INTERFACE
    def update_attendee(self, attendee_id: int, data: dict) -> Optional[Attendee]:
        """
        Update an attendee by ID with partial data.
        """
        return self.repo.update(attendee_id, data)

    # PUBLIC_INTERFACE
    def delete_attendee(self, attendee_id: int) -> bool:
        """
        Delete attendee by ID.
        """
        return self.repo.delete(attendee_id)
