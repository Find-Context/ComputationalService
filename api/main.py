from fastapi import FastAPI

from .middleware.exception_middleware import GlobalExceptionMiddleware
from .routes import api_router
app = FastAPI()
app.add_middleware(GlobalExceptionMiddleware)
app.include_router(api_router)
