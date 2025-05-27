from fastapi import APIRouter, HTTPException, Path, Form
from app.models.event import Event, EventPublic, EventCreate
from app.data.db import SessionDep
from sqlmodel import select

router = APIRouter(prefix="/events")

@router.get("/")
def get_events_list(
        session: SessionDep
) -> list[EventPublic]:
    """Returns the list of events."""
    statement = select(Event)
    events = session.exec(statement).all()
    return events