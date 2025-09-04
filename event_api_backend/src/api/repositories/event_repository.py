from typing import List, Optional, Tuple

from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import Session, joinedload

from ..models.event import Event


class EventRepository:
    """
    Repository for CRUD operations on Event entities.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, event: Event) -> Event:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get(self, event_id: int) -> Optional[Event]:
        stmt = select(Event).options(joinedload(Event.attendees)).where(Event.id == event_id)
        return self.db.execute(stmt).scalars().first()

    def list(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> Tuple[List[Event], int]:
        base_stmt = select(Event).options(joinedload(Event.attendees))
        count_stmt = select(func.count()).select_from(Event)

        if search:
            like_term = f"%{search}%"
            base_stmt = base_stmt.where(Event.title.ilike(like_term))
            count_stmt = count_stmt.where(Event.title.ilike(like_term))

        total = self.db.execute(count_stmt).scalar_one()
        events = self.db.execute(base_stmt.order_by(Event.start_time.asc()).offset(skip).limit(limit)).scalars().all()
        return events, total

    def update(self, event_id: int, data: dict) -> Optional[Event]:
        if not data:
            return self.get(event_id)
        stmt = (
            update(Event)
            .where(Event.id == event_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        result = self.db.execute(stmt)
        if result.rowcount == 0:
            return None
        self.db.commit()
        return self.get(event_id)

    def delete(self, event_id: int) -> bool:
        stmt = delete(Event).where(Event.id == event_id)
        result = self.db.execute(stmt)
        self.db.commit()
        return result.rowcount > 0
