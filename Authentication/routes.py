from fastapi import APIRouter, HTTPException, Body
from config import db
from model import User

user=APIRouter()

@user.post("/auth/signup")
async def signup(new_user: User):
    # Check if a user with the same username or email already exists
    existing_user = db['user'].find_one({"$or": [{"username": new_user.username}, {"email": new_user.email}]})

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already in use")

    else:
        # Insert the new user into the collection
        db['user'].insert_one(dict(new_user))

        return {"message": "User created successfully"}
    
@user.post("/auth/login")
async def login(username: str = Body(...), password: str = Body(...)):
    # Find a user with the provided username and password
    user = db['user'].find_one({"username": username, "password": password})

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    else:
        return {"name": user["username"]}