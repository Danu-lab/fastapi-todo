from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.api.v1 import todos, auth

app = FastAPI(
    title="FastAPI ToDo App",
    description="Simple ToDo App with JWT Auth, CRUD, and PostgreSQL",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "url": "https://website.com",
    },
    openapi_tags=[
        {"name": "auth", "description": "Authentication & Registration"},
        {"name": "todos", "description": "CRUD operations for your tasks"},
    ]
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(todos.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

@app.get("/health", tags=["system"])
@limiter.limit("5/minute")
def health_check(request: Request):
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI ToDo API"}
