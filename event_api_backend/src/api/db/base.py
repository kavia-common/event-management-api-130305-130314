import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Read DB URL from environment; fallback to local SQLite file.
# Do not hardcode sensitive info. Users can set DATABASE_URL in the environment (.env).
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./event_db.sqlite3")

# For SQLite, need check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy session and ensures proper close.

    Yields:
        Session: SQLAlchemy session bound to configured engine.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PUBLIC_INTERFACE
def init_db() -> None:
    """
    Initialize the database by creating all tables defined in the models.
    """
    # Import models to ensure metadata is populated
    from ..models.event import Event  # noqa: F401
    from ..models.attendee import Attendee  # noqa: F401
    Base.metadata.create_all(bind=engine)
