# Library Management System

A modern library management system built with FastAPI and SQLAlchemy, featuring book tracking, student management, and automated email reminders.

## Features

- Book management (add, update, delete, search)
- Student management
- Book issuance and return tracking
- Automated email reminders for overdue books
- RESTful API endpoints
- Database integration
- Email notifications using Mailtrap.io

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation and settings management
- **Python 3.8+**: Core programming language
- **Alembic**: Database migration tool

### Database
- **PostgreSQL**: Primary database
- **SQLAlchemy ORM**: Object-Relational Mapping

### Email Service
- **Mailtrap.io**: Email testing and delivery service
- **SMTP**: For sending automated email reminders

## Project Structure

```
library/
├── api/                    # API endpoints
│   ├── v1/                # API version 1
│   │   ├── books.py       # Book endpoints
│   │   ├── students.py    # Student endpoints
│   │   └── issues.py      # Book issue endpoints
│   └── __init__.py
├── models/                # SQLAlchemy models
│   ├── book.py           # Book model
│   ├── student.py        # Student model
│   └── issue.py          # Book issue model
├── schemas/              # Pydantic models/schemas
│   ├── book.py          # Book schemas
│   ├── student.py       # Student schemas
│   └── issue.py         # Issue schemas
├── crud/                # Database operations
│   ├── book.py         # Book CRUD operations
│   ├── student.py      # Student CRUD operations
│   └── issue.py        # Issue CRUD operations
├── services/           # Business logic
│   └── reminder_service.py  # Email reminder service
├── config.py          # Configuration settings
├── database.py        # Database connection
├── main.py           # FastAPI application
├── send.py           # Email sending utility
├── test_email.py     # Email testing script
└── requirements.txt   # Project dependencies
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- Mailtrap.io account (for email testing)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd library
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/library_db
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USERNAME=your_mailtrap_username
EMAIL_PASSWORD=your_mailtrap_password
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
- `GET /books`: List all books
- `POST /books`: Add a new book
- `GET /books/{id}`: Get book details
- `PUT /books/{id}`: Update book
- `DELETE /books/{id}`: Delete book

### Students
- `GET /students`: List all students
- `POST /students`: Add a new student
- `GET /students/{id}`: Get student details
- `PUT /students/{id}`: Update student
- `DELETE /students/{id}`: Delete student

### Book Issues
- `POST /issues`: Issue a book
- `PUT /issues/{id}/return`: Return a book
- `GET /issues`: List all book issues
- `GET /issues/{id}`: Get issue details

## Email Reminders

The system automatically sends email reminders for:
- Books due in 5 days
- Overdue books

Email configuration uses Mailtrap.io for testing. In production, update the email settings to use your preferred email service provider.

## Database Schema

### Books
- id (Primary Key)
- title
- author
- isbn
- total_copies
- available_copies
- category
- created_at
- updated_at

### Students
- id (Primary Key)
- name
- roll_number
- department
- semester
- phone
- email
- created_at
- updated_at

### Book Issues
- id (Primary Key)
- book_id (Foreign Key)
- student_id (Foreign Key)
- issue_date
- expected_return_date
- return_date
- is_returned
- is_overdue
- created_at
- updated_at

## Security

- Input validation using Pydantic models
- SQL injection prevention through SQLAlchemy
- Environment variable protection
- Email authentication

## Testing

Run tests using:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.