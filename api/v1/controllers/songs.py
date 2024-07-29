from fastapi.responses import JSONResponse
from pydantic import BaseModel


class SongRequest(BaseModel):
    url: str


async def root() -> JSONResponse:
    return JSONResponse(content={"message": "/api/v1"})

async def add_song(request: SongRequest) -> JSONResponse:
    return JSONResponse(content={"url": request.url})

async def get_song(song_id: str) -> JSONResponse:
    return JSONResponse(content={"song_id": song_id})
