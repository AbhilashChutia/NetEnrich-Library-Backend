import smtplib
from email.mime.text import MIMEText
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from models.issue import BookIssue
from models.student import Student
from models.book import Book
from database import get_session
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM_ADDRESS
import asyncio

async def send_email(to_email: str, subject: str, body: str):
    if not all([EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM_ADDRESS]):
        print("Email configuration incomplete. Skipping email sending.")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls() 
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {to_email} for subject: {subject}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

async def check_and_send_reminders():
    print("Running check_and_send_reminders...")
    async for session in get_session():
        today = date.today()
        five_days_from_now = today + timedelta(days=5)

        stmt = select(BookIssue, Student, Book).join(Student).join(Book).where(
            BookIssue.is_returned == False,
            BookIssue.expected_return_date <= five_days_from_now
        )
        result = await session.execute(stmt)
        issues_to_remind = result.all()

        for issue, student, book in issues_to_remind:
            subject = ""
            body = ""
            if issue.expected_return_date <= today:
                if not issue.is_overdue:
                    issue.is_overdue = True
                    session.add(issue) 
                    await session.commit()
                    await session.refresh(issue)

                subject = f"OVERDUE: Library Book Reminder - {book.title}"
                body = (
                    f"Dear {student.name},\n\n"
                    f"This is a reminder that the book '{book.title}' (ISBN: {book.isbn}) "
                    f"was due on {issue.expected_return_date}. Please return it as soon as possible.\n\n"
                    "Thank you,\nCollege Library"
                )
            elif issue.expected_return_date > today and issue.expected_return_date <= five_days_from_now:
                subject = f"Upcoming Due Date: Library Book - {book.title}"
                body = (
                    f"Dear {student.name},\n\n"
                    f"This is a reminder that the book '{book.title}' (ISBN: {book.isbn}) "
                    f"is due on {issue.expected_return_date}. Please return it on or before this date.\n\n"
                    "Thank you,\nCollege Library"
                )

            if subject and body:
                await send_email(student.email, subject, body)