from typing import List, Optional, Tuple

from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import Session

from ..models.attendee import Attendee


class AttendeeRepository:
    """
    Repository for CRUD operations on Attendee entities.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, attendee: Attendee) -> Attendee:
        self.db.add(attendee)
        self.db.commit()
        self.db.refresh(attendee)
        return attendee

    def get(self, attendee_id: int) -> Optional[Attendee]:
        stmt = select(Attendee).where(Attendee.id == attendee_id)
        return self.db.execute(stmt).scalars().first()

    def list(self, event_id: Optional[int] = None, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> Tuple[List[Attendee], int]:
        base_stmt = select(Attendee)
        count_stmt = select(func.count()).select_from(Attendee)

        if event_id is not None:
            base_stmt = base_stmt.where(Attendee.event_id == event_id)
            count_stmt = count_stmt.where(Attendee.event_id == event_id)

        if search:
            like_term = f"%{search}%"
            base_stmt = base_stmt.where(Attendee.name.ilike(like_term))
            count_stmt = count_stmt.where(Attendee.name.ilike(like_term))

        total = self.db.execute(count_stmt).scalar_one()
        attendees = self.db.execute(base_stmt.order_by(Attendee.created_at.desc()).offset(skip).limit(limit)).scalars().all()
        return attendees, total

    def update(self, attendee_id: int, data: dict) -> Optional[Attendee]:
        if not data:
            return self.get(attendee_id)
        stmt = (
            update(Attendee)
            .where(Attendee.id == attendee_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        result = self.db.execute(stmt)
        if result.rowcount == 0:
            return None
        self.db.commit()
        return self.get(attendee_id)

    def delete(self, attendee_id: int) -> bool:
        stmt = delete(Attendee).where(Attendee.id == attendee_id)
        result = self.db.execute(stmt)
        self.db.commit()
        return result.rowcount > 0
