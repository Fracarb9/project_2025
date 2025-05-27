from fastapi import APIRouter, HTTPException, Path, Form
from app.models.event import Event, EventPublic, EventCreate
from app.data.db import SessionDep
from sqlmodel import select

router = APIRouter(prefix="/events")

@router.get("/")
def get_events_list(
        session: SessionDep
) -> list[EventPublic]:
    """Returns the list of existing events"""
    statement = select(Event)
    events = session.exec(statement).all()
    return events

@router.post("/")
def create_event(event:EventCreate, session: SessionDep):
    """Creates a new event."""
    new_event = Event.model_validate(event)
    session.add(new_event)
    session.commit()
    return "Event successfully created"

@router.get("/{id}")
def get_event_by_id(
        id: int,
        session: SessionDep
) -> EventPublic:
    """Returns the event with the given id."""
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{id}")
def update_event(
        session: SessionDep,
        id: int,
        new_event: EventCreate,
):
    """Updates an existing event."""
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    event.title = new_event.title
    event.description = new_event.description
    event.date = new_event.date
    event.location = new_event.location
    session.add(event)
    session.commit()
    return "Event successfully updated"

@router.delete("/{id}")
def delete_event(
        session: SessionDep,
        id: int
):
    """Deletes an existing event."""
    event = session.get(Event, id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()
    return "Event successfully deleted"