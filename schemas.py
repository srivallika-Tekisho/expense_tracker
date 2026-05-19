from pydantic import BaseModel, Field
import datetime
from typing import Optional


class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    category: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    date: Optional[datetime.date] = None


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    date: Optional[datetime.date] = None


class ExpenseOut(BaseModel):
    id: int
    amount: float
    category: str
    description: Optional[str]
    date: datetime.date

    class Config:
        from_attributes = True


class SummaryOut(BaseModel):
    total_spent: float
    total_expenses: int
    by_category: dict[str, float]
