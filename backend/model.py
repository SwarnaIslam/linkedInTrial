from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str = ""
    roll: Optional[str] = None
    batch: Optional[str] = None
    session: Optional[str] = None
    program_level: Optional[str] = None
    mobile_number: str = ""
    address: Optional[str] = None
    email: str = ""
    password: str = ""
    status: str = ""
    role: str = ""


class POSTS(BaseModel):
    image_name:str=""
    username:str=""
    text:str=""