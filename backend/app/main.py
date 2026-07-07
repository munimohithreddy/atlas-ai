from fastapi import FastAPI

app = FastAPI(
    title="Atlas AI",
    description="AI-powered publishing and affiliate marketing platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Atlas AI",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }