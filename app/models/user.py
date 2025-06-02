from sqlmodel import SQLModel, Field


class UserCreate(SQLModel):
    username: str
    name: str
    email: str



class UserPublic(UserCreate):
    pass



class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    name: str
    email: str
