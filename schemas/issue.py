from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, datetime

class IssueBase(BaseModel):
    book_id: UUID
    student_id: UUID
    expected_return_date: date

class IssueCreate(IssueBase):
    pass

class IssueReturn(BaseModel):
    return_date: Optional[date] = None 

class Issue(IssueBase):
    id: UUID
    issue_date: date
    return_date: Optional[date] = None
    is_returned: bool
    is_overdue: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True