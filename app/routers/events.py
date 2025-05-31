from fastapi import APIRouter, HTTPException, Path, Form
from sqlmodel import select
from app.models.user import User
from app.models.registration import Registration, RegisterUserRequest
from app.models.event import Event, EventPublic, EventCreate
from app.data.db import SessionDep


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


@router.delete("/", status_code=204)
def delete_all_events(db: SessionDep):
    events = db.exec(select(Event)).all()

    if not events:
        raise HTTPException(status_code=404, detail="No events to delete.")

    for event in events:
        db.delete(event)
    db.commit()


@router.post("/{id}/register")
def register_user_to_event(
    id: int = Path(..., description="Event ID"),
    user_data: RegisterUserRequest = ...,
    db: SessionDep = None
):
    """Registers a new user to an event by ID."""


    event = db.exec(select(Event).where(Event.id == id)).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")


    user = db.exec(select(User).where(User.username == user_data.username)).first()
    if not user:
        user = User(
            username=user_data.username,
            name=user_data.name,
            email=user_data.email
        )
        db.add(user)
        db.commit()
        db.refresh(user)


    registration = db.exec(
        select(Registration).where(
            (Registration.username == user_data.username) &
            (Registration.event_id == id)
        )
    ).first()
    if registration:
        raise HTTPException(status_code=400, detail="User already registered")


    registration = Registration(username=user_data.username, event_id=id)
    db.add(registration)
    db.commit()

    return {"message": "Registration successful"}