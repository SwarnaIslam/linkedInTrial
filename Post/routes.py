from fastapi import APIRouter, HTTPException, UploadFile, Form, File
from datetime import datetime, timezone
from minio import Minio
import io
import uuid
from config import post_db
from model import POSTS
from schemas import postEntity, postsEntity
from bson import ObjectId
import pika
import json

import asyncio
posting=APIRouter()


rabbitmq_host = "rabbitmq"
rabbitmq_port = 5672  
rabbitmq_user = "admin" 
rabbitmq_password = "admin123"  

def get_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            credentials=pika.credentials.PlainCredentials(
                username=rabbitmq_user,
                password=rabbitmq_password,
            ),
        )
    )
    
    channel = connection.channel()
    
    channel.exchange_declare(
        exchange="post",
        exchange_type="direct"
    )
    return connection, channel
@posting.on_event('startup')
async def startup():
    await asyncio.sleep(30)
    connection, channel=get_rabbitmq()
    connection.close()

@posting.get("/post", response_model=list[POSTS])
def get_posts():
    try:
        posts = post_db['post'].find()
        post_list = postsEntity(posts)

        return post_list

    except Exception as error:
        raise HTTPException(status_code=500, detail="Internal server error")

@posting.get('/post/{postId}', response_model=POSTS)
async def get_post(postId: str):
    try:
        post = post_db['post'].find_one({"_id": ObjectId(postId)})

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return postEntity(post)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Internal server error")


@posting.post("/post")
async def add_post(username: str = Form(None),
    texts: str = Form(None),
    image_file: UploadFile = File(None)):
    try:
        image_url=""
        if image_file:
            image_url = await upload_image(image_file, username)
        result = post_db['post'].insert_one({
            "username": username,
            "texts": texts,
            "image_url": image_url
        })
        post_id = result.inserted_id

        # Create notification message
        message = "Added an image!"
        if texts:
            message = texts[:70]

        notification_data = {
            "username": username,
            "postId": str(post_id),
            "timestamp": datetime.now().astimezone(timezone.utc).isoformat(),
            "message": message
        }

        connection,channel= get_rabbitmq()
        
        channel.basic_publish(
            exchange='post',
            routing_key='post.notify',
            body=json.dumps(notification_data)
        )
        connection.close()
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Internal server error")

# Define your proxy configuration
proxy_host = 'minio'
proxy_port = 9000

# Create an HTTP client session with proxy settings
from urllib3 import make_headers
from urllib3 import ProxyManager

proxy_headers = make_headers(proxy_basic_auth='username:password')  # If your proxy requires authentication
http_client = ProxyManager(
    proxy_url=f"http://{proxy_host}:{proxy_port}",
    proxy_headers=proxy_headers
)

# Create a Minio client with the configured HTTP client
minio_client = Minio(
    "localhost:9000",
    access_key="lala",
    secret_key="lala1212",
    http_client=http_client,  # Set the custom HTTP client with proxy settings
    secure=False,
)

async def upload_image(imgFile,username:str):
    bucket_name = "linkedin"
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    file_bytes = await imgFile.read()
    unique_filename = username+str(uuid.uuid4()) + "_" + imgFile.filename

    file_stream = io.BytesIO(file_bytes)

    minio_client.put_object(
        "linkedin",
        unique_filename,
        file_stream,
        length=len(file_bytes),
        content_type=imgFile.content_type,
    )

    presigned_url = minio_client.presigned_get_object('linkedin', unique_filename)
    print(presigned_url)
    return presigned_url