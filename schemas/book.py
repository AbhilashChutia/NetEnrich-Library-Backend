from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    category: str

class BookCreate(BookBase):
    total_copies: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    total_copies: Optional[int] = None
    category: Optional[str] = None

class Book(BookBase):
    id: UUID
    total_copies: int
    available_copies: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True