from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from database import get_session
from schemas.book import BookCreate, BookUpdate, Book
from crud.book import book_crud

router = APIRouter()

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_new_book(book_in: BookCreate, db: AsyncSession = Depends(get_session)):
    db_book = await book_crud.get_book_by_isbn(db, book_in.isbn)
    if db_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this ISBN already exists"
        )
    return await book_crud.create_book(db=db, book_in=book_in)

@router.get("/", response_model=List[Book])
async def list_books(
    title: str | None = None,
    author: str | None = None,
    category: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)
):
    skip = (page - 1) * limit
    books = await book_crud.get_books(
        db=db,
        title=title,
        author=author,
        category=category,
        skip=skip,
        limit=limit
    )
    return books

@router.get("/{book_id}", response_model=Book)
async def get_book_details(book_id: UUID, db: AsyncSession = Depends(get_session)):
    db_book = await book_crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_book

@router.put("/{book_id}", response_model=Book)
async def update_existing_book(
    book_id: UUID, book_in: BookUpdate, db: AsyncSession = Depends(get_session)
):
    db_book = await book_crud.update_book(db=db, book_id=book_id, book_in=book_in)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_book(book_id: UUID, db: AsyncSession = Depends(get_session)):
    success = await book_crud.delete_book(db=db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return