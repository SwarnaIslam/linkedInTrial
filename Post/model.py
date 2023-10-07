from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional, List
class POSTS(BaseModel):
    id: str
    username: str
    image_url: str
    texts: str

class NewPost(BaseModel):
    username:str
    image_file:Optional[UploadFile]=None
    texts: Optional[List[str]] = []