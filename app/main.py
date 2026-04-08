from fastapi import FastAPI
from .routes import api_router
from middleware import message_exception_handler

app = FastAPI()
app.middleware("http")(message_exception_handler)
app.include_router(api_router)