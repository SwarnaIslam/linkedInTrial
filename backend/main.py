from model import User
import os
from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from pydantic import BaseModel
from typing import Optional
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile


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


