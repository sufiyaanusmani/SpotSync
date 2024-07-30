from typing import TYPE_CHECKING

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.core.config import SessionLocal
from api.services.db import store_song_in_db
from api.services.spotify import get_song_metadata

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class SongRequest(BaseModel):
    url: str


async def root() -> JSONResponse:
    return JSONResponse(content={"message": "/api/v1"})

async def add_song(request: SongRequest) -> JSONResponse:
    metadata = get_song_metadata(request.url)
    if "error" in metadata:
        raise HTTPException(status_code=400, detail=metadata["error"])

    # Store metadata in SQLite database using SQLAlchemy
    db: Session = SessionLocal()
    db_song = store_song_in_db(db, metadata)
    db.close()
    return db_song

async def get_song(song_id: str) -> JSONResponse:
    return JSONResponse(content={"song_id": song_id})
