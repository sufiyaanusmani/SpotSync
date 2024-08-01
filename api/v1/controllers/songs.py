from typing import TYPE_CHECKING

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.core.config import SessionLocal
from api.models.models import Song
from api.services.db import store_song_in_db
from api.services.spotify import get_song_metadata

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class SongRequest(BaseModel):
    url: str

class UpdateStatusRequest(BaseModel):
    status: str


async def root() -> JSONResponse:
    return JSONResponse(content={"message": "/api/v1"})

async def add_song(request: Request, song_request: SongRequest) -> JSONResponse:
    metadata = get_song_metadata(song_request.url)
    if "error" in metadata:
        raise HTTPException(status_code=400, detail=metadata["error"])

    # Store metadata in SQLite database using SQLAlchemy
    db: Session = SessionLocal()
    db_song = store_song_in_db(db, metadata)
    db.close()
    return {
        "id": db_song.id,
        "name": db_song.name,
        "artists": db_song.artists,
        "album": db_song.album,
        "release_date": db_song.release_date,
        "duration": db_song.duration,
        "url": db_song.url,
        "thumbnail_url": db_song.thumbnail_url,
        "status": db_song.status,
        "download_url": str(request.url_for("get_song", song_id=db_song.id))
    }

async def get_song_info(song_id: str) -> JSONResponse:
    db: Session = SessionLocal()
    song = db.query(Song).filter(Song.id == song_id).first()
    if song:
        return song
    return JSONResponse(status_code=404, content={"message": "Song not found"})


async def get_all_songs_info() -> JSONResponse:
    db: Session = SessionLocal()
    songs = db.query(Song).all()
    db.close()
    return songs
