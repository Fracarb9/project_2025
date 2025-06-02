from fastapi import APIRouter, Depends, HTTPException
from app.data.db import SessionDep
from sqlmodel import select
from app.models.registration import RegistrationPublic
from app.models.registration import Registration

router = APIRouter(prefix="/registrations")

@router.get("/", response_model=list[RegistrationPublic])
def get_all_registrations(db:SessionDep):
    registrations = db.exec(select(Registration)).all()
    return registrations
@router.delete("/")
def delete_registration(
    username: str,
    event_id: int,
    session: SessionDep
):
    """Deletes a registration"""

    registration = session.exec(
        select(Registration).where(
            (Registration.username == username) &
            (Registration.event_id == event_id)
        )
    ).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    session.delete(registration)
    session.commit()
    return {"message": "Registration successfully deleted"}

