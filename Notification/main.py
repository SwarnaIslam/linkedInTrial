from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app=FastAPI()

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
        database="linkedin_notification"
    )
    return db


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