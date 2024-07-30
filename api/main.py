from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from api.constants.directory import MEDIA_DIR, SONG_DIR
from api.core.config import engine
from api.models.models import Base
from api.v1.routes import routes

# Create an instance of the FastAPI class
app = FastAPI()

# Serve static files from the "media" directory
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

app.include_router(routes.router, prefix="/api/v1")

# Create tables
@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)

# Define a route for the root URL ("/")
@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}

@app.get("/media/songs/{song_id}.mp3")
async def get_song(song_id: str) -> FileResponse:
    file_path = SONG_DIR / f"{song_id}.mp3"

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"},
    )

# Run the application using 'uvicorn' if this script is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) # uvicorn api.main:app --reload
