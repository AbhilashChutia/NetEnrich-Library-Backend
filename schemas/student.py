from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date

class StudentBase(BaseModel):
    name: str
    roll_number: str
    department: str
    semester: int
    phone: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    semester: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class Student(StudentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IssuedBookDetail(BaseModel):
    issue_id: UUID
    book_id: UUID
    title: str
    author: str
    isbn: str
    issue_date: date
    expected_return_date: date
    return_date: Optional[date] = None
    is_overdue: bool 
    class Config:
        from_attributes = True

class StudentIssuedBooks(BaseModel):
    student_id: UUID
    name: str
    roll_number: str
    department: str
    semester: int
    phone: str
    email: EmailStr
    issued_books: List[IssuedBookDetail] = []

    class Config:
        from_attributes = True