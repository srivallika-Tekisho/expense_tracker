from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import expenses

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker",
    description="A simple API to record, categorize, and analyze your spending.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Expense Tracker API is running 🚀"}
