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
    scheduler.add_job(check_and_send_reminders, 'interval', seconds=10)
    scheduler.start()
    print("Scheduler started.")

    yield

    print("Shutting down scheduler...")
    scheduler.shutdown()
    print("Scheduler shut down.")

app = FastAPI(
    title="College Library Management System",
    description="Backend system for managing books, students, and book insurance.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan 
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the College Library API!"}