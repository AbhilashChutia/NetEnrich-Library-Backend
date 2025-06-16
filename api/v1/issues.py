from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from typing import List
from uuid import UUID
from datetime import date

from database import get_session
from schemas.issue import IssueCreate, IssueReturn, Issue 
from schemas.student import IssuedBookDetail
from crud.issue import issue_crud
from crud.book import book_crud
from crud.student import student_crud
from models.issue import BookIssue 

router = APIRouter()

@router.post("/", response_model=Issue, status_code=status.HTTP_201_CREATED)
async def issue_book_to_student(issue_in: IssueCreate, db: AsyncSession = Depends(get_session)):
    book = await book_crud.get_book(db, issue_in.book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    student = await student_crud.get_student(db, issue_in.student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    if book.available_copies <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No available copies of this book")
    
    db_issue = await issue_crud.issue_book(db=db, issue_in=issue_in)
    if db_issue is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to issue book")
    return db_issue

@router.put("/{issue_id}/return", response_model=Issue)
async def return_issued_book(
    issue_id: UUID,
    issue_return_data: IssueReturn = IssueReturn(), 
    db: AsyncSession = Depends(get_session)
):
   
    db_issue_result = await db.execute(select(BookIssue).filter(BookIssue.id == issue_id))
    existing_issue = db_issue_result.scalars().first()
    
    if not existing_issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue record not found")
    
    if existing_issue.is_returned:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already returned")

    returned_issue = await issue_crud.return_book(
        db=db,
        issue_id=issue_id,
        actual_return_date=issue_return_data.return_date 
    )
    if returned_issue is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to return book")
    return returned_issue

@router.get("/active", response_model=List[Issue])
async def list_all_active_issues(db: AsyncSession = Depends(get_session)):
    active_issues = await issue_crud.get_all_active_issues(db=db)
    return active_issues

@router.get("/student/{student_id}", response_model=List[IssuedBookDetail])
async def list_books_issued_to_student(student_id: UUID, db: AsyncSession = Depends(get_session)):
    student = await student_crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    issued_books = await issue_crud.get_issued_books_for_student(db=db, student_id=student_id)
    return issued_books



