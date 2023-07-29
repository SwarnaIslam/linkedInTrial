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
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

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
async def login(username: str = Body(), password: str = Body()):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM user WHERE username = %s AND password = %s"
    values = (username, password)
    cursor.execute(query, values)

    result = cursor.fetchone()

    if result is None:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")
    else:
        return {'name': result[0]}


# Route to create a new user [DONE]
@app.post("/signup")
async def signup(user: User, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    # Check if the username or email is already in use
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s", (user.username, user.email))
    result = cursor.fetchone()

    if result:
        raise HTTPException(status_code=400, detail="Username or email already in use")

    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)",
                       (user.username, user.email, user.password))
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
async def upload_image(username:str=Form(None), thumbnail: UploadFile = File(None)):
    file_bytes = await thumbnail.read()
    unique_filename = username+str(uuid.uuid4()) + "_" + thumbnail.filename

    file_stream = io.BytesIO(file_bytes)

    minio_client.put_object(
        "linkedin",
        unique_filename,
        file_stream,
        length=len(file_bytes),
        content_type=thumbnail.content_type,
    )

    presigned_url = minio_client.presigned_get_object('linkedin', unique_filename)
    return {"token": presigned_url}

@app.post("/add-post")
async def add_post(post:POSTS):
    try:
        db = get_db()
        cursor = db.cursor()
        postSql = "INSERT INTO posts (image_name, username, texts) VALUES (%s, %s, %s)"
        values = (post.image_name, post.username, post.texts)
        cursor.execute(postSql, values)
        postId=cursor.lastrowid
        message="Added an image!"
        if post.texts:
            message=post.texts[:70]

        currentTime=datetime.now()
        notifySql="INSERT INTO notifications (username, postId, timestamp, message) VALUES(%s,%s,%s,%s)"
        values=(post.username, postId, currentTime, message)

        cursor.execute(notifySql, values)
        db.commit()
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        cursor.close()
        db.close()
    return {"message": "Post added successfully"}

@app.get("/all-posts", response_model=list[POSTS])
def get_posts():
    # MySQL Connection
    db = get_db()
    cursor = db.cursor()

    # Query
    query = "SELECT * FROM posts"

    # Execute Query
    cursor.execute(query)

    # Get all rows that match the search criteria
    posts = cursor.fetchall()
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
    return post_list

@app.get('/get-post/{postId}', response_model=POSTS)
async def get_post(postId:int):
    # MySQL Connection
    db = get_db()
    cursor = db.cursor()

    # Query
    query = "SELECT * FROM posts WHERE postId=%s"
    # Execute Query
    cursor.execute(query,(postId,))

    # Get all rows that match the search criteria
    post = cursor.fetchone()
    return {
            "image_name": post[1],
            "username": post[2],
            "texts": post[3]
        }


@app.get('/notification/{username}')
async def get_notifications(username:str):
    # MySQL Connection
    db = get_db()
    cursor = db.cursor()
    one_hour_ago=datetime.now()-timedelta(hours=1)

    # Query
    query = "SELECT * FROM notifications WHERE username != %s AND timestamp>=%s"

    # Execute Query
    cursor.execute(query,(username,one_hour_ago))

    # Get all rows that match the search criteria
    notifications = cursor.fetchall()
    notification_list = []
    for notification in notifications:
        # Define the format of the input datetime string
        input_format = "%Y-%m-%d %H:%M:%S"
        notification_list.append({
            "username": notification[1],
            "postId":notification[2],
            "timestamp": notification[3].strftime(input_format),
            "message": notification[4]
        })

    # Close the database connection
    cursor.close()
    db.close()
    print(datetime.now())
        # Return the list of unapproved users as a JSON response
    return notification_list

# Add the notification cleaner job
def clean_notifications():
    one_hour_ago = datetime.now() - timedelta(hours=1)
    delete_query = "DELETE FROM notifications WHERE timestamp <= %s"
    db = get_db()
    cursor = db.cursor()
    cursor.execute(delete_query, (one_hour_ago,))
    db.commit()
    cursor.close()

# Schedule the notification cleaner job to run every hour (you can adjust the interval as needed)
scheduler = BackgroundScheduler()
scheduler.add_job(clean_notifications, 'interval', minutes=1)
scheduler.start()