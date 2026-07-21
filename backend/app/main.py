from fastapi import FastAPI

app = FastAPI(
    title="Bus Marketplace API",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Bus Marketplace!",
        "status": "Running Successfully"
    }