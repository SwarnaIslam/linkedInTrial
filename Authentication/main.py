from fastapi import Body, FastAPI, HTTPException,Form
from fastapi.params import Depends
import mysql.connector
from pydantic import BaseModel
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

# define a database connection function
def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="linkedin_user"
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