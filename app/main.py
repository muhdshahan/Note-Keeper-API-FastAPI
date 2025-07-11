from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.db.database import engine, Base
from app.routers import notes, auth
from app.core.logging_config import setup_logging
from app.core.exception_handlers import (
    validation_exception_handler,
    http_exception_handler,
    integrity_error_handler,
    generic_exception_handler,
)
from app.core.limiter import limiter  # ✅ Import shared limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

# 🔧 Setup logging
setup_logging()

# 🎯 Create FastAPI instance
app = FastAPI(
    title="Note-Keeping API",
    description="A secure API for notes with JWT authentication and rate limiting",
    version="2.0.0"
)

# ✅ Register rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# 🔗 Include routers
app.include_router(auth.router)
app.include_router(notes.router)

# ⚠️ Custom exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# 🔄 On startup: create DB tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 🏠 Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure Note-Keeping API!"}