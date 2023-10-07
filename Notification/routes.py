from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from config import notification_db
from schemas import notificationsEntity
from apscheduler.schedulers.background import BackgroundScheduler
import aio_pika
import json
import asyncio

# RabbitMQ server hostname (service name in Docker Compose)
rabbitmq_host = "rabbitmq"
rabbitmq_port = 5672  # Default RabbitMQ port
rabbitmq_user = "admin"  # Use the username from your environment variables
rabbitmq_password = "admin123"  # Use the password from your environment variables

notification=APIRouter()

@notification.on_event('startup')
async def startup_event():
    await asyncio.sleep(35)
    try:
        connection = await aio_pika.connect_robust(
            host=rabbitmq_host,
            port=rabbitmq_port,
            login=rabbitmq_user,
            password=rabbitmq_password,
        )

        channel = await connection.channel()
        
        queue = await channel.declare_queue('post_notify')
        await queue.bind('post', 'post.notify')
        await queue.consume(add_notification)
        print("Consuming messages...")

    except Exception as error:
        print(error)

@notification.get('/notification/{username}')
async def get_notifications(username: str):
    try:
        # Calculate one hour ago from the current datetime
        one_hour_ago = datetime.now() - timedelta(hours=1)

        # Find notifications with the specified username and timestamp less than or equal to one hour ago
        notifications = notification_db['notification'].find(
            {"username": {"$ne": username}, "timestamp": {"$gte": one_hour_ago.isoformat()}}
        )
        print(one_hour_ago)
        return notificationsEntity(notifications)

    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Internal server error")
    
async def add_notification(message: aio_pika.IncomingMessage):
    try:
        notification = json.loads(message.body)
        await message.ack()
        print(notification)
        notification_db['notification'].insert_one(notification)
        print("notification added!")

    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Internal server error")
    

def clean_notifications():
    try:
        one_hour_ago = datetime.now() - timedelta(hours=1)

        # Delete notifications with a timestamp greater than or equal to one hour ago
        notification_db['notification'].delete_many({"timestamp": {"$lte": one_hour_ago.isoformat()}})

    except Exception as error:
        print(error)


# Schedule the notification cleaner job to run every hour (you can adjust the interval as needed)
scheduler = BackgroundScheduler()
scheduler.add_job(clean_notifications, 'interval', minutes=0.5)
scheduler.start()