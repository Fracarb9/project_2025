from sqlmodel import SQLModel, Field

class EventBase(SQLModel):
    name: str
    description: str

class Event(EventBase, table=True):
    id: int = Field(default=None, primary_key=True)

class EventCreate(EventBase):
    pass

class EventPublic(EventBase):
    id: int
