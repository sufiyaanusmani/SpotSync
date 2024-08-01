from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from api.constants.songs import Status

Base = declarative_base()

class Song(Base):
    __tablename__ = "songs"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    artists = Column(String)
    album = Column(String)
    release_date = Column(String)
    duration = Column(Integer)
    url = Column(String, unique=True, index=True)
    thumbnail_url = Column(String)
    status = Column(String, index=True, default=Status.NOT_STARTED)
    next_check_time = Column(DateTime, index=True, nullable=True, default=None)
