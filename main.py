from fastapi import FastAPI

from api.auth_router import router as auth_router

app = FastAPI()


app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/health")
def health_check() -> dict[str, str]:
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok"}
