from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, field_validator

from .attendee import AttendeeRead


class EventBase(BaseModel):
    title: str = Field(..., description="Title of the event", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Optional description of the event")
    location: Optional[str] = Field(None, description="Location of the event", max_length=255)
    start_time: datetime = Field(..., description="Start datetime of the event in ISO format")
    end_time: datetime = Field(..., description="End datetime of the event in ISO format")

    @field_validator("end_time")
    @classmethod
    def validate_times(cls, v, values):
        start = values.get("start_time")
        if start and v <= start:
            raise ValueError("end_time must be after start_time")
        return v


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the event", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Optional description of the event")
    location: Optional[str] = Field(None, description="Location of the event", max_length=255)
    start_time: Optional[datetime] = Field(None, description="Start datetime of the event in ISO format")
    end_time: Optional[datetime] = Field(None, description="End datetime of the event in ISO format")

    @field_validator("end_time")
    @classmethod
    def validate_times(cls, v, values):
        start = values.get("start_time")
        # Only validate if both are provided in update payload
        if v is not None and start is not None and v <= start:
            raise ValueError("end_time must be after start_time")
        return v


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Event ID")
    title: str = Field(..., description="Title of the event")
    description: Optional[str] = Field(None, description="Optional description")
    location: Optional[str] = Field(None, description="Location of the event")
    start_time: datetime = Field(..., description="Start datetime")
    end_time: datetime = Field(..., description="End datetime")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    attendees: List[AttendeeRead] = Field(default_factory=list, description="List of attendees for the event")
