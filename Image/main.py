import io
from fastapi import FastAPI,Form,File, UploadFile, HTTPException
import mysql.connector
from pydantic import BaseModel
from minio import Minio
import uuid
from fastapi.middleware.cors import CORSMiddleware

class User(BaseModel):
    username: str = ""
    email: str = ""
    password: str = ""

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:8080",
    "http://localhost:4200"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MinIO client configuration
minio_client = Minio(
    "127.0.0.1:9000",  # MinIO server address
    access_key="EsCAeDi5YXtJoaoXoOSI",
    secret_key="4yRy6oiALNkaeVQX5kTobyxAgld28eRDhOzhW8cP",
    secure=False,  # Set to True if using HTTPS
)


# define a database connection function
def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="linkedin_image"
    )
    return db
@app.post("/thumbnail-upload")
async def upload_image(username: str = Form(None), thumbnail: UploadFile = File(None)):
    if thumbnail is None:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if thumbnail.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_bytes = await thumbnail.read()
    unique_filename = username + str(uuid.uuid4()) + "_" + thumbnail.filename

    file_stream = io.BytesIO(file_bytes)

    minio_client.put_object(
        "linkedin",
        unique_filename,
        file_stream,
        length=len(file_bytes),
        content_type=thumbnail.content_type,
    )

    presigned_url = minio_client.presigned_get_object(
        "linkedin", unique_filename
    )

    return {"token": presigned_url}
