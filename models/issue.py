import uuid
from sqlalchemy import Column, ForeignKey, Date, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class BookIssue(Base):
    __tablename__ = "book_issues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    issue_date = Column(Date, nullable=False, server_default=func.now())
    expected_return_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    is_returned = Column(Boolean, nullable=False, default=False)
    is_overdue = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    book = relationship("Book", backref="issues")
    student = relationship("Student", backref="issues")

    def __repr__(self):
        return (f"<BookIssue(book_id='{self.book_id}', student_id='{self.student_id}', "
                f"issue_date='{self.issue_date}', is_returned='{self.is_returned}')>")