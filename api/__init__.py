from fastapi import APIRouter
from .v1 import books, students, issues

router = APIRouter()
router.include_router(books.router, prefix="/books", tags=["Books"])
router.include_router(students.router, prefix="/students", tags=["Students"])
router.include_router(issues.router, prefix="/issues", tags=["Book Issues"])