from fastapi import FastAPI
from .routes import message_router
from middleware import message_exception_handler

app = FastAPI()
app.middleware("http")(message_exception_handler)
app.include_router(message_router)
