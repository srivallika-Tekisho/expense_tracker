# 💸 Expense Tracker API

A simple FastAPI + PostgreSQL project to **record, categorize, and analyze** your spending.

---

## 📁 Project Structure

```
expense_tracker/
├── main.py            # App entry point
├── database.py        # DB connection & session
├── models.py          # SQLAlchemy table model
├── schemas.py         # Pydantic request/response schemas
├── routers/
│   └── expenses.py    # All expense routes
├── requirements.txt
└── .env.example
```

---

## ⚙️ Setup

### 1. Clone & install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create your `.env` file
```bash
cp .env.example .env
```
Edit `.env` and set your PostgreSQL connection string:
```
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/expense_tracker
```

### 3. Create the database (if it doesn't exist)
```sql
CREATE DATABASE expense_tracker;
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

The API will be live at **http://localhost:8000**
Interactive docs at **http://localhost:8000/docs**

---

## 📌 API Endpoints

| Method   | Route                      | Description                        |
|----------|----------------------------|------------------------------------|
| `GET`    | `/`                        | Health check                       |
| `POST`   | `/expenses/`               | Add a new expense                  |
| `GET`    | `/expenses/`               | List all expenses (with filters)   |
| `GET`    | `/expenses/{id}`           | Get a single expense               |
| `PATCH`  | `/expenses/{id}`           | Update an expense                  |
| `DELETE` | `/expenses/{id}`           | Delete an expense                  |
| `GET`    | `/expenses/summary/overview` | Spending summary & by-category analytics |

---

## 🔍 Query Filters

### List expenses
```
GET /expenses/?category=food&from_date=2024-01-01&to_date=2024-01-31
```

### Summary
```
GET /expenses/summary/overview?from_date=2024-01-01&to_date=2024-01-31
```

---

## 📝 Example Requests

### Add an expense
```json
POST /expenses/
{
  "amount": 12.50,
  "category": "Food",
  "description": "Lunch at cafe",
  "date": "2024-05-19"
}
```

### Summary response
```json
{
  "total_spent": 245.75,
  "total_expenses": 12,
  "by_category": {
    "Food": 85.50,
    "Transport": 60.00,
    "Shopping": 100.25
  }
}
```
