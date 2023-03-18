from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    # to validate payload post content
    id: Optional[int] = None
    title: str
    category: str
    content: str
    author: str
    published: bool = True  # optional field with default value
    like: Optional[int] = None
    created_at: Optional[int] = None


class PatchPost(Post):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
