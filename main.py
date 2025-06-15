from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from api import router as api_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.reminder_service import check_and_send_reminders
import asyncio

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    await init_db()
    print("Database initialized.")

    print("Starting scheduler...")
    # Schedule to run at 10 AM every day
    scheduler.add_job(check_and_send_reminders, 'cron', hour=10, minute=0)
    # scheduler.add_job(check_and_send_reminders, 'interval', hours=24)

    scheduler.start()
    print("Scheduler started.")

    yield

    print("Shutting down scheduler...")
    scheduler.shutdown()
    print("Scheduler shut down.")

app = FastAPI(
    title="NetEnrich College Library Management System",
    description="Backend system for managing books, students, and book issuance.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Abhilash",
        "email": "abhilashchutia1999@gmail.com"
    },
    license_info={
        "name": "MIT"
    },
    lifespan=lifespan 
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the NetEnrich College Library Backend API!"}