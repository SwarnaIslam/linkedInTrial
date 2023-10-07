from fastapi import FastAPI
from routes import posting
app=FastAPI()
app.include_router(posting)