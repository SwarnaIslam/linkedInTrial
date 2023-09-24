import io
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Optional
import mysql.connector
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

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
# define a database connection function
def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="linkedin_post"
    )
    return db

class POSTS(BaseModel):
    image_name:Optional[str]=None
    username:str=""
    texts:Optional[str]=None

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