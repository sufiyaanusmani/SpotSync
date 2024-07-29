from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.v1.routes import routes

# Create an instance of the FastAPI class
app = FastAPI()
app.include_router(routes.router, prefix="/api/v1")

# Define a route for the root URL ("/")
@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"},
    )

# Run the application using 'uvicorn' if this script is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
