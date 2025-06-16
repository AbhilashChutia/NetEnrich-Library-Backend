# Library Management System

A modern library management system built with FastAPI and SQLAlchemy, featuring
book tracking, student management, and automated email reminders.

## Features

-   Book management (add, update, delete, search)
-   Student management
-   Book issuance and return tracking
-   Automated email reminders for overdue books
-   RESTful API endpoints
-   Database integration

## Tech Stack

### Backend

-   **FastAPI**: Modern, fast web framework for building APIs
-   **SQLAlchemy**: SQL toolkit and ORM
-   **Pydantic**: Data validation and settings management
-   **Python 3.8+**: Core programming language
-   **Alembic**: Database migration tool

### Database

-   **PostgreSQL**: Primary database
-   **SQLAlchemy ORM**: Object-Relational Mapping

### Email Service

-   **SMTP**: For sending automated email reminders

## Project Structure

```
library/
├── api/
│   ├── v1/
│   │   ├── books.py
│   │   ├── students.py
│   │   └── issues.py
│   └── __init__.py
├── models/
│   ├── book.py
│   ├── student.py
│   └── issue.py
├── schemas/
│   ├── book.py
│   ├── student.py
│   └── issue.py
├── crud/
│   ├── book.py
│   ├── student.py
│   └── issue.py
├── services/
│   └── reminder_service.py
├── config.py
├── database.py
├── main.py
└── requirements.txt
```

## Getting Started

### Prerequisites

-   Python 3.8 or higher
-   PostgreSQL database

### Installation

1. Clone the repository:

```bash
git clone https://github.com/AbhilashChutia/NetEnrich-Library-Backend.git
cd NetEnrich-Library-Backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables: Create a `.env` file in the root directory with
   the following variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/library_db
EMAIL_HOST=smtp.io
EMAIL_PORT=2525
EMAIL_USERNAME=your_username
EMAIL_PASSWORD=your_password
EMAIL_FROM_ADDRESS=library@yourdomain.com
```

5. Run database migrations:

```bash
alembic upgrade head
```

6. Start the application:

```bash
uvicorn main:app --reload
```

## API Endpoints

### Books

-   `GET /books`: List all books
-   `POST /books`: Add a new book
-   `GET /books/{book_id}`: Get book details
-   `PUT /books/{book_id}`: Update book
-   `DELETE /books/{book_id}`: Delete book

### Students

-   `GET /students`: List all students
-   `POST /students`: Add a new student
-   `GET /students/{student_id}`: Get student details
-   `PUT /students/{student_id}`: Update student
-   `DELETE /students/{student_id}`: Delete student

### Book Issues

-   `POST /issues`: Issue a book
-   `PUT /issues/{issue_id}/return`: Return a book
-   `GET /issues/active`: List all book issues
-   `GET /issues/{issue_id}`: Get issue details

## Email Reminders

The system automatically sends email reminders for:

-   Books due in 5 days
-   Overdue books

In production, update the email settings to use your preferred email service
provider.

## Database Schema

### Books

-   id (Primary Key)
-   title
-   author
-   isbn
-   total_copies
-   available_copies
-   category
-   created_at
-   updated_at

### Students

-   id (Primary Key)
-   name
-   roll_number
-   department
-   semester
-   phone
-   email
-   created_at
-   updated_at

### Book Issues

-   id (Primary Key)
-   book_id (Foreign Key)
-   student_id (Foreign Key)
-   issue_date
-   expected_return_date
-   return_date
-   is_returned
-   is_overdue
-   created_at
-   updated_at

## Security

-   Input validation using Pydantic models
-   Environment variable protection
-   Email authentication
