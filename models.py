"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

# TODO: Complete your models

class User(Base):
    __tablename__ = "users"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    password = Column("password", TEXT, nullable=False)
    age = Column("age", INTEGER, nullable=False)
    gender = Column("gender", TEXT, nullable=False)
    zipcode = Column("zipcode", INTEGER, nullable=False)
    language = Column("language", TEXT, nullable=False)
    experience = Column("experience", TEXT, nullable=False)
    bio = Column("bio", TEXT, nullable=True)

    def __repr__(self):
        return repr(self.name)

class Session(Base):
    __tablename__ = "sessions"

    #Columns
    id = Column("id", INTEGER, primary_key=True, autoincrement=True)
    time = Column("time", TEXT)
    month = Column("month", TEXT, nullable=False)
    day = Column("day", INTEGER, nullable=False)
    location = Column("location", TEXT, nullable=False)
    accepted = Column("accepted", TEXT, nullable=False)

class UserSession(Base):
    __tablename__ = "user_session"

    #Columns
    id = Column("id", INTEGER, primary_key=True, autoincrement=True)
    user_id = Column("user_id", INTEGER, ForeignKey('users.id'))
    session_id = Column("session_id", INTEGER, ForeignKey('sessions.id'))
    requester_id = Column("requester", INTEGER)