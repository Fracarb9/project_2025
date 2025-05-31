from fastapi import APIRouter, Depends
from app.data.db import SessionDep
from sqlmodel import select
from app.models.registration import RegistrationPublic
from app.models.registration import Registration

router = APIRouter(prefix="/registrations")

@router.get("/", response_model=list [RegistrationPublic])
def get_all_registrations(db:SessionDep):
    registrations = db.exec(select(Registration)).all()
    return registrations

