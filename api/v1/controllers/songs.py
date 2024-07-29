from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.services.spotify import get_song_metadata


class SongRequest(BaseModel):
    url: str


async def root() -> JSONResponse:
    return JSONResponse(content={"message": "/api/v1"})

async def add_song(request: SongRequest) -> JSONResponse:
    metadata = get_song_metadata(request.url)
    if "error" in metadata:
        raise HTTPException(status_code=400, detail=metadata["error"])
    return metadata

async def get_song(song_id: str) -> JSONResponse:
    return JSONResponse(content={"song_id": song_id})
