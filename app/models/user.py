from sqlmodel import SQLModel, Field


# modello per input da API POST/users
class UserCreate(SQLModel):
    username: str
    name: str
    email: str


# modello per risposta API GET /users
class UserPublic(UserCreate):
    pass


# modello per il database
class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    name: str
    email: str
