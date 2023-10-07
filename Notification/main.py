from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import notification

app=FastAPI()
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:8080",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notification)

