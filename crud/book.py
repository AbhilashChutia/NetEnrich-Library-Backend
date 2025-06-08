from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional
from uuid import UUID

from models.book import Book
from schemas.book import BookCreate, BookUpdate

class CRUDBook:
    async def create_book(self, db: AsyncSession, book_in: BookCreate) -> Book:
        db_book = Book(
            title=book_in.title,
            author=book_in.author,
            isbn=book_in.isbn,
            total_copies=book_in.total_copies,
            available_copies=book_in.total_copies,
            category=book_in.category
        )
        db.add(db_book)
        await db.commit()
        await db.refresh(db_book)
        return db_book

    async def get_book(self, db: AsyncSession, book_id: UUID) -> Optional[Book]:
        result = await db.execute(select(Book).filter(Book.id == book_id))
        return result.scalars().first()

    async def get_book_by_isbn(self, db: AsyncSession, isbn: str) -> Optional[Book]:
        result = await db.execute(select(Book).filter(Book.isbn == isbn))
        return result.scalars().first()

    async def get_books(
        self,
        db: AsyncSession,
        title: Optional[str] = None,
        author: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Book]:
        query = select(Book)
        conditions = []
        if title:
            conditions.append(Book.title.ilike(f"%{title}%"))
        if author:
            conditions.append(Book.author.ilike(f"%{author}%"))
        if category:
            conditions.append(Book.category == category)

        if conditions:
            query = query.where(and_(*conditions))

        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def update_book(
        self, db: AsyncSession, book_id: UUID, book_in: BookUpdate
    ) -> Optional[Book]:
        db_book = await self.get_book(db, book_id)
        if not db_book:
            return None

        if book_in.total_copies is not None:
            old_total_copies = db_book.total_copies
            diff = book_in.total_copies - old_total_copies
            db_book.available_copies += diff
            db_book.available_copies = max(0, db_book.available_copies)

        for var, value in book_in.model_dump(exclude_unset=True).items():
            setattr(db_book, var, value)

        await db.commit()
        await db.refresh(db_book)
        return db_book

    async def delete_book(self, db: AsyncSession, book_id: UUID) -> bool:
        db_book = await self.get_book(db, book_id)
        if not db_book:
            return False
        await db.delete(db_book)
        await db.commit()
        return True

book_crud = CRUDBook()