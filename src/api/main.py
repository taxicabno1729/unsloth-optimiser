from fastapi import FastAPI

app = FastAPI(title="Unsloth Optimiser API", version="0.1.0")


@app.get("/")
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}