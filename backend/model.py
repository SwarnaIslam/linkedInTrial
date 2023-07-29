from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str = ""
    email: str = ""
    password: str = ""


class POSTS(BaseModel):
    image_name:Optional[str]=None
    username:str=""
    texts:Optional[str]=None