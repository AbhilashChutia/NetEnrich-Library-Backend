from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from typing import List, Optional
from uuid import UUID

from models.student import Student
from schemas.student import StudentCreate, StudentUpdate

class CRUDStudent:
    async def create_student(self, db: AsyncSession, student_in: StudentCreate) -> Student:
        db_student = Student(
            name=student_in.name,
            roll_number=student_in.roll_number,
            department=student_in.department,
            semester=student_in.semester,
            phone=student_in.phone,
            email=student_in.email
        )
        db.add(db_student)
        await db.commit()
        await db.refresh(db_student)
        return db_student

    async def get_student(self, db: AsyncSession, student_id: UUID) -> Optional[Student]:
        result = await db.execute(select(Student).filter(Student.id == student_id))
        return result.scalars().first()

    async def get_student_by_identifier(self, db: AsyncSession, identifier: str) -> Optional[Student]:
        try:
            student_id = UUID(identifier)
            result = await db.execute(select(Student).filter(Student.id == student_id))
            return result.scalars().first()
        except ValueError:
            result = await db.execute(
                select(Student).filter(
                    or_(
                        Student.name.ilike(f"%{identifier}%"),
                        Student.roll_number.ilike(f"%{identifier}%"),
                        Student.phone.ilike(f"%{identifier}%")
                    )
                )
            )
            return result.scalars().first()


    async def get_students(
        self,
        db: AsyncSession,
        department: Optional[str] = None,
        semester: Optional[int] = None,
        query_str: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Student]:
        query = select(Student)
        conditions = []

        if department:
            conditions.append(Student.department == department)
        if semester:
            conditions.append(Student.semester == semester)
        if query_str:
            conditions.append(
                or_(
                    Student.name.ilike(f"%{query_str}%"),
                    Student.roll_number.ilike(f"%{query_str}%"),
                    Student.phone.ilike(f"%{query_str}%")
                )
            )

        if conditions:
            query = query.where(and_(*conditions))

        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def update_student(
        self, db: AsyncSession, student_id: UUID, student_in: StudentUpdate
    ) -> Optional[Student]:
        db_student = await self.get_student(db, student_id)
        if not db_student:
            return None

        for var, value in student_in.model_dump(exclude_unset=True).items():
            setattr(db_student, var, value)

        await db.commit()
        await db.refresh(db_student)
        return db_student

    async def delete_student(self, db: AsyncSession, student_id: UUID) -> bool:
        db_student = await self.get_student(db, student_id)
        if not db_student:
            return False
        await db.delete(db_student)
        await db.commit()
        return True

student_crud = CRUDStudent()