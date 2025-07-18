from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    # slug is optional, generated behind the scenes, so you don't send it from client
    slug: Optional[str] = None

class PostOut(PostBase):
    id: int
    slug: str

    class Config:
        orm_mode = True
