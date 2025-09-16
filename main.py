from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check() -> dict[str, str]:
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok"}
