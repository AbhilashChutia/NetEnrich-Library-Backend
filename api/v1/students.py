from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from database import get_session
from schemas.student import StudentCreate, StudentUpdate, Student, StudentIssuedBooks
from crud.student import student_crud
from crud.issue import issue_crud 

router = APIRouter()

@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_new_student(student_in: StudentCreate, db: AsyncSession = Depends(get_session)):
    existing_student_roll = await student_crud.get_students(db, query_str=student_in.roll_number, limit=1)
    if existing_student_roll:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student with this roll number already exists")
    
    existing_student_phone = await student_crud.get_students(db, query_str=student_in.phone, limit=1)
    if existing_student_phone:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student with this phone number already exists")

    return await student_crud.create_student(db=db, student_in=student_in)

@router.get("/", response_model=List[Student])
async def list_students(
    department: str | None = None,
    semester: int | None = None,
    query: str | None = None, 
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)
):
    skip = (page - 1) * limit
    students = await student_crud.get_students(
        db=db,
        department=department,
        semester=semester,
        query_str=query,
        skip=skip,
        limit=limit
    )
    return students

@router.get("/{student_id}", response_model=Student)
async def get_student_details(student_id: UUID, db: AsyncSession = Depends(get_session)):
    db_student = await student_crud.get_student(db=db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return db_student

@router.put("/{student_id}", response_model=Student)
async def update_existing_student(
    student_id: UUID, student_in: StudentUpdate, db: AsyncSession = Depends(get_session)
):
    db_student = await student_crud.update_student(db=db, student_id=student_id, student_in=student_in)
    if db_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return db_student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_student(student_id: UUID, db: AsyncSession = Depends(get_session)):
    success = await student_crud.delete_student(db=db, student_id=student_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return

@router.get("/issued-books/", response_model=StudentIssuedBooks)
async def get_student_issued_books(
    identifier: str, 
    db: AsyncSession = Depends(get_session)
):
    db_student = await student_crud.get_student_by_identifier(db, identifier)
    if db_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found with provided identifier")
    
    issued_books_details = await issue_crud.get_issued_books_for_student(db, db_student.id)
    
    return StudentIssuedBooks(
        student_id=db_student.id,
        name=db_student.name,
        roll_number=db_student.roll_number,
        department=db_student.department,
        semester=db_student.semester,
        phone=db_student.phone,
        email=db_student.email,
        issued_books=issued_books_details
    )