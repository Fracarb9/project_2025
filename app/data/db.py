from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config
# Importati: remember to import all the DB models here
from app.models.registration import Registration  # NOQA
from app.models.user import User
from app.models.event import Event
from sqlalchemy import event


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:

            # Complete: (optional) initialize the database with fake data
            for i in range(5): #Creazione fittizia di utenti in caso di DB vuoto
                user = User(
                    username=f.user_name(),
                    name=f.name(),
                    email=f.email()
                )
                session.add(user)
            session.commit()

            for i in range(5): #Creazione fittizia di eventi in caso di DB vuoto
                event = Event(
                    title = f.catch_phrase(),  #Breve frase
                    description = f.paragraph(nb_sentences=3), #Paragrafetto
                    date = f.future_datetime(end_date="+2y"),
                    location = f.city(),
                    id = None
                )
                session.add(event)
            session.commit()



def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
