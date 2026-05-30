# FreelanceHub

A modern web platform that connects freelancers with clients and agencies in a unified ecosystem.

## Run locally
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy + Alembic |
| Authentication | JWT (python-jose) |
| Cache | Redis |
| Background Jobs | Celery |
| AI Module | Groq API (llama-3.3-70b-versatile) |
| Frontend | React + Vite + Context API |
| Testing | Pytest (9/9 passing) |
| CI/CD | GitHub Actions |


## Project Structure
freelancehub/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── schemas/s
│   │   ├── middleware/
│   │   ├── tasks/         
│   │   └── cache.py      
│   ├── alembic/    
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/     
│       ├── context/  
│       └── services/   
├── .github/
│   └── workflows/
│       └── ci.yml     
└── README.md

## Setup

### Requirements
- Python 3.11+
- PostgreSQL
- Redis
- Node.js 18+

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
# Fill in your environment variables
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Celery Worker

```bash
cd backend
celery -A app.tasks.celery_app worker --loglevel=info --pool=solo
```

## API Documentation

After starting the server, open:

http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc

## Testing

```bash
cd backend
pytest app/tests/ -v
```

Result: **9/9 tests passing**

## CI/CD

GitHub Actions automatically runs on every push:
1. Install dependencies
2. Start Redis service
3. Run all tests
4. Verify health check

## Author
Developed as part of the Distributed Systems 2025/26 course.