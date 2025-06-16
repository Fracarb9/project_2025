from sqlmodel import SQLModel, Field, Column
from sqlalchemy import ForeignKey

class Registration(SQLModel, table=True):
    username: str = Field(
        sa_column=Column("username",
                         ForeignKey("user.username", ondelete="CASCADE"),
                         primary_key=True)
    )
    event_id: int = Field(
        sa_column=Column("event_id",
                         ForeignKey("event.id", ondelete="CASCADE"),
                         primary_key=True)
    )


class RegistrationPublic(SQLModel):
    username: str
    event_id: int

class RegisterUserRequest(SQLModel):
    username: str
    name: str
    email: str