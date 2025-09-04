from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class AttendeeBase(BaseModel):
    name: str = Field(..., description="Full name of the attendee", min_length=1, max_length=255)
    email: EmailStr = Field(..., description="Valid email address of the attendee")


class AttendeeCreate(AttendeeBase):
    event_id: int = Field(..., description="ID of the event the attendee belongs to")


class AttendeeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Full name of the attendee", min_length=1, max_length=255)
    email: Optional[EmailStr] = Field(None, description="Valid email address of the attendee")


class AttendeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Attendee ID")
    event_id: int = Field(..., description="Event ID")
    name: str = Field(..., description="Full name of the attendee")
    email: EmailStr = Field(..., description="Email address of the attendee")
    created_at: datetime = Field(..., description="Creation timestamp")
