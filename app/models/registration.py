from sqlmodel import SQLModel, Field



class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username")
    event_id: int = Field(primary_key=True, foreign_key="event.id")


class RegistrationPublic(SQLModel):
    username: str
    event_id: int

class RegisterUserRequest(SQLModel):
    username: str
    name: str
    email: str