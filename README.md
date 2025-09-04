# event-management-api-130305-130314

This workspace provides a FastAPI backend container `event_api_backend` implementing a REST API to manage events and attendees. No authorization is required.

## Features

- CRUD endpoints for Events and Attendees
- SQLite persistence by default (SQLAlchemy ORM)
- Input validation with Pydantic (including date/time constraints)
- Proper error handling and meaningful HTTP status codes
- OpenAPI documentation at `/docs` and `/openapi.json`
- CORS enabled for all origins (development friendly)

## Run locally

From the container root:

```bash
cd event_api_backend
# Optional: create a virtualenv
# python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001
```

Open http://localhost:3001/docs to explore the API.

## Configuration

- The app uses SQLite by default and creates `event_db.sqlite3` in the working directory.
- To use another database, provide `DATABASE_URL` (see `.env.example` for guidance). Make sure the appropriate driver is installed.

## API Overview

- Health: `GET /`
- Events:
  - `POST /api/events` — Create event
  - `GET /api/events` — List events
  - `GET /api/events/{event_id}` — Get event by ID
  - `PATCH /api/events/{event_id}` — Update event
  - `DELETE /api/events/{event_id}` — Delete event
- Attendees:
  - `POST /api/attendees` — Create attendee
  - `GET /api/attendees` — List attendees; filter by `event_id`
  - `GET /api/attendees/{attendee_id}` — Get attendee by ID
  - `PATCH /api/attendees/{attendee_id}` — Update attendee
  - `DELETE /api/attendees/{attendee_id}` — Delete attendee

All endpoints return JSON responses and include validation and basic error handling.
