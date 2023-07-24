from model import User,POSTS
import os
import io
from fastapi import Body, FastAPI, HTTPException,Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from pydantic import BaseModel
from typing import Optional
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
from minio import Minio
import uuid


app = FastAPI()

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


# define a database connection function
def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="e_library"
    )
    return db


# define a login endpoint [DONE]
@app.post("/login")
async def login(email: str = Body(), password: str = Body()):
    db = get_db()
    cursor = db.cursor()
    print("Working...")
    query = "SELECT * FROM user WHERE email = %s AND password = %s"
    values = (email, password)
    cursor.execute(query, values)

    result = cursor.fetchone()

    if result is None:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")
    else:
        return {'name': result[0], 'role': result[10]}


# Route to create a new user [DONE]
@app.post("/signup")
async def signup(user: User, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    # Check if the username or email is already in use
    print("RESULT: ", user)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user WHERE name = %s OR email = %s", (user.name, user.email))
    result = cursor.fetchone()

    if result:
        raise HTTPException(status_code=400, detail="Username or email already in use")

    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO user (name, roll, batch, session, program_level, mobile_number, address, email, password, status, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (user.name, user.roll, user.batch, user.session, user.program_level, user.mobile_number, user.address, user.email, user.password, user.status, user.role))
        db.commit()

        return {"User created successfully"}

# MinIO client configuration
minio_client = Minio(
    "127.0.0.1:9000",  # MinIO server address
    access_key="EsCAeDi5YXtJoaoXoOSI",
    secret_key="4yRy6oiALNkaeVQX5kTobyxAgld28eRDhOzhW8cP",
    secure=False,  # Set to True if using HTTPS
)

@app.post("/thumbnail-upload")
async def create_file(username:str=Form(None), thumbnail: UploadFile = File(None)):
    print(username)
    file_bytes = await thumbnail.read()
    unique_filename = username+"_"+str(uuid.uuid4()) + "_" + thumbnail.filename

    file_stream = io.BytesIO(file_bytes)

    minio_client.put_object(
        "linkedin",
        unique_filename,
        file_stream,
        length=len(file_bytes),
        content_type=thumbnail.content_type,
    )

    return {"token": unique_filename}

@app.post("/add-post")
async def add_post(post:POSTS):
    try:
        db = get_db()
        cursor = db.cursor()
        sql = "INSERT INTO posts (image_name, username, texts) VALUES (%s, %s, %s)"
        values = (post.image_name, post.username, post.texts)
        cursor.execute(sql, values)
        db.commit()
    # except mysql.connector.Error as error:
    #     print("Error connecting to database: ", error)
    #     raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        cursor.close()
        db.close()
    return {"message": "Post added successfully"}

# Get all unapproved users [DONE]
@app.get("/posts/all-posts", response_model=list[POSTS])
def get_posts():
    # MySQL Connection
    print("getting users")
    db = get_db()
    cursor = db.cursor()

    # Query
    query = "SELECT * FROM posts"

    # Execute Query
    cursor.execute(query)

    # Get all rows that match the search criteria
    posts = cursor.fetchall()

    # Check if any users were found
    if len(posts) == 0:
        return JSONResponse(content={"message": "No unapproved users found"})
    else:
        # Convert the result to a list of User objects
        post_list = []
        for post in posts:
            post_list.append({
                "image_name": post[1],
                "username": post[2],
                "texts": post[3]
            })

        # Close the database connection
        cursor.close()
        db.close()

        # Return the list of unapproved users as a JSON response
        print(post_list)
        return post_list