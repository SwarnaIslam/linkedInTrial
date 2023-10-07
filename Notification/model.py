from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId
class Notification(BaseModel):
    postId: str
    username:str
    message:str
    timeStamp: datetime