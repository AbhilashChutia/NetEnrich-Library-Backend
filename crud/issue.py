from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from uuid import UUID
from datetime import date

from models.issue import BookIssue
from models.book import Book
from models.student import Student
from schemas.issue import IssueCreate
from schemas.student import IssuedBookDetail

class CRUDIssue:
    async def issue_book(self, db: AsyncSession, issue_in: IssueCreate) -> Optional[BookIssue]:
        db_book = await db.execute(select(Book).filter(Book.id == issue_in.book_id))
        book = db_book.scalars().first()

        db_student = await db.execute(select(Student).filter(Student.id == issue_in.student_id))
        student = db_student.scalars().first()

        if not book or not student:
            return None 

        if book.available_copies <= 0:
            return None 

        db_issue = BookIssue(
            book_id=issue_in.book_id,
            student_id=issue_in.student_id,
            expected_return_date=issue_in.expected_return_date,
            issue_date=date.today(), 
            is_returned=False,
            is_overdue=False 
        )
        db.add(db_issue)
        book.available_copies -= 1 

        await db.commit()
        await db.refresh(db_issue)
        await db.refresh(book)
        return db_issue

    async def return_book(self, db: AsyncSession, issue_id: UUID, actual_return_date: Optional[date] = None) -> Optional[BookIssue]:
        db_issue = await db.execute(select(BookIssue).filter(BookIssue.id == issue_id))
        issue = db_issue.scalars().first()

        if not issue:
            return None

        if issue.is_returned:
            return None 

        book = await db.execute(select(Book).filter(Book.id == issue.book_id))
        db_book = book.scalars().first()

        issue.return_date = actual_return_date if actual_return_date else date.today()
        issue.is_returned = True
        issue.is_overdue = False 

        if db_book:
            db_book.available_copies += 1

        await db.commit()
        await db.refresh(issue)
        if db_book:
            await db.refresh(db_book)
        return issue

    async def get_issued_books_for_student(self, db: AsyncSession, student_id: UUID) -> List[IssuedBookDetail]:
        stmt = select(BookIssue, Book).join(Book).where(
            BookIssue.student_id == student_id,
            BookIssue.is_returned == False 
        )
        result = await db.execute(stmt)
        issued_books = []
        today = date.today()

        for issue, book in result.all():
            is_book_overdue = issue.expected_return_date < today
            issued_books.append(
                IssuedBookDetail(
                    issue_id=issue.id,
                    book_id=book.id,
                    title=book.title,
                    author=book.author,
                    isbn=book.isbn,
                    issue_date=issue.issue_date,
                    expected_return_date=issue.expected_return_date,
                    return_date=issue.return_date,
                    is_overdue=is_book_overdue 
                )
            )
        return issued_books
    
    async def get_all_active_issues(self, db: AsyncSession) -> List[BookIssue]:
        stmt = select(BookIssue).where(BookIssue.is_returned == False)
        result = await db.execute(stmt)
        return result.scalars().all()


issue_crud = CRUDIssue()