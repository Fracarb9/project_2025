from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select, delete
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
    return "User successfully created"

@router.delete("/")
def delete_all_users(session: SessionDep):
    """Deletes all users."""
    statement = delete(User)
    session.exec(statement)
    session.commit()
    return "All users successfully deleted"

@router.get("/{username}", response_model=UserPublic)
def get_user_by_username(
    session: SessionDep,
    username: str
) -> UserPublic:
    """Returns the user with the given username."""
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{username}")
def delete_user(
    session: SessionDep,
    username :str
):
    """Deletes the user with the given ID."""
    user = session.get(User, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return "User successfully deleted"