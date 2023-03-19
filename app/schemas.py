from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    # to validate payload post content
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True  # optional field with default value
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


class PatchPost(Post):
    title: Optional[str] = None
    content: Optional[str] = None
