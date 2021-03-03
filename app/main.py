from fastapi import FastAPI
from api.api import api_router
from starlette.middleware.cors import CORSMiddleware
from db.session import engine
from models import setting


setting.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router)