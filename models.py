from sqlalchemy import Column, Integer, Float, String, Text, Date
from sqlalchemy.sql import func
from database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(Date, server_default=func.current_date(), nullable=False)
