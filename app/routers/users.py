from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.data.db import SessionDep
from app.models.user import User, UserCreate, UserPublic

router = APIRouter(prefix="/users")


@router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Returns all users"""
    statement = select(User)
    users = session.exec(statement).all()
    return users


@router.post("/")
def create_user(user_create: UserCreate, session: SessionDep):
    """Creates a new user."""
    existing_user = session.exec(
        select(User).where(User.username == user_create.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User.model_validate(user_create)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
