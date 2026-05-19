from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date

from database import get_db
from models import Expense
from schemas import ExpenseCreate, ExpenseUpdate, ExpenseOut, SummaryOut

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# ── Add an expense ────────────────────────────────────────────────────────────
@router.post("/", response_model=ExpenseOut, status_code=201)
def create_expense(payload: ExpenseCreate, db: Session = Depends(get_db)):
    expense = Expense(**payload.model_dump(exclude_none=True))
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


# ── List all expenses (with optional filters) ─────────────────────────────────
@router.get("/", response_model=list[ExpenseOut])
def list_expenses(
    category: Optional[str] = Query(None, description="Filter by category"),
    from_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    query = db.query(Expense)

    if category:
        query = query.filter(Expense.category.ilike(f"%{category}%"))
    if from_date:
        query = query.filter(Expense.date >= from_date)
    if to_date:
        query = query.filter(Expense.date <= to_date)

    return query.order_by(Expense.date.desc()).all()


# ── Summary / Analytics ───────────────────────────────────────────────────────
@router.get("/summary/overview", response_model=SummaryOut)
def get_summary(
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Expense)

    if from_date:
        query = query.filter(Expense.date >= from_date)
    if to_date:
        query = query.filter(Expense.date <= to_date)

    expenses = query.all()

    total_spent = sum(e.amount for e in expenses)
    total_expenses = len(expenses)

    by_category: dict[str, float] = {}
    for e in expenses:
        by_category[e.category] = round(by_category.get(e.category, 0) + e.amount, 2)

    return SummaryOut(
        total_spent=round(total_spent, 2),
        total_expenses=total_expenses,
        by_category=by_category,
    )


# ── Get a single expense ──────────────────────────────────────────────────────
@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


# ── Update an expense ─────────────────────────────────────────────────────────
@router.patch("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, payload: ExpenseUpdate, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


# ── Delete an expense ─────────────────────────────────────────────────────────
@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
