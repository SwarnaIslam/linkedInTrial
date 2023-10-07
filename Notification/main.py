from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import notification

app=FastAPI()
app.include_router(notification)

