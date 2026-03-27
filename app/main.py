from fastapi import FastAPI
from routes import api_router

app = FastAPI()

app.add_middleware(
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)#TODO: implement cors middleware
app.include_router(api_router)
