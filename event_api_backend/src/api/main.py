from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.events import router as events_router
from .routes.attendees import router as attendees_router
from .db.base import init_db

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance with routers registered.
    """
    app = FastAPI(
        title="Event Management API",
        description="RESTful API to manage events and attendees. No authorization required.",
        version="1.0.0",
        openapi_tags=[
            {"name": "health", "description": "Health check endpoint"},
            {"name": "events", "description": "Operations related to events"},
            {"name": "attendees", "description": "Operations related to attendees"},
        ],
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health route
    @app.get("/", tags=["health"], summary="Health Check")
    def health_check():
        """
        Health check endpoint.

        Returns:
            JSON with a simple 'Healthy' message to indicate the service is running.
        """
        return {"message": "Healthy"}

    # Include routers
    app.include_router(events_router, prefix="/api", tags=["events"])
    app.include_router(attendees_router, prefix="/api", tags=["attendees"])

    # Initialize database (create tables if they don't exist)
    init_db()

    return app


app = create_app()
