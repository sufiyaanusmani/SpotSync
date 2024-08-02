from typing import TYPE_CHECKING

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from api.constants.directory import Directory
from api.constants.songs import CHECK_UNDOWNLOADED_SONGS_INTERVAL_SEC
from api.core.config import SessionLocal, engine
from api.models.models import Base
from api.services.download import process_undownloaded_songs
from api.v1.routes import routes

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

# Create an instance of the FastAPI class
app = FastAPI()
scheduler = BackgroundScheduler()

# Serve static files from the "media" directory
app.mount("/media", StaticFiles(directory=Directory.MEDIA_DIR), name="media")

app.include_router(routes.router, prefix="/api/v1")

def download_undownloaded_songs() -> None:
    db: Session = SessionLocal()
    try:
        process_undownloaded_songs(db)
    finally:
        db.close()

# Create tables
@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    scheduler.add_job(download_undownloaded_songs, "interval", seconds=CHECK_UNDOWNLOADED_SONGS_INTERVAL_SEC, max_instances=1)
    scheduler.start()

# Define a route for the root URL ("/")
@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}

@app.get("/media/songs/{song_id}.mp3")
async def get_song(song_id: str) -> FileResponse:
    file_path = Directory.SONG_DIR / f"{song_id}.mp3"

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"},
    )

@app.on_event("shutdown")
async def shutdown_event() -> None:
    scheduler.shutdown()

# Run the application using 'uvicorn' if this script is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) # uvicorn api.main:app --reload
