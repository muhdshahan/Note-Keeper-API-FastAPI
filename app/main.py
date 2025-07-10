from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import notes

app = FastAPI(
    title="Note-Keeping API",
    description="A simple API for creating and managing notes",
    version="1.0.0"
)

# Include only notes router
app.include_router(notes.router)

# Create database tables on startup (sync version)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Note-Keeping API!"}
