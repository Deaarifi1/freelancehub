from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, projects, bids, contracts, payments, reviews, messages, ai, agencies, search
from app.middleware.logging import LoggingMiddleware
from app.middleware.tenant import TenantMiddleware
from app.config import settings

app = FastAPI(
    title="FreelanceHub API",
    description="Platformë moderne për lidhjen e freelancerëve me klientët",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(TenantMiddleware)

# Routers (20+ endpoints)
app.include_router(auth.router)        # /auth/*
app.include_router(users.router)       # /users/*
app.include_router(projects.router)    # /projects/*
app.include_router(bids.router)        # /bids/*
app.include_router(contracts.router)   # /contracts/*
app.include_router(payments.router)    # /payments/*
app.include_router(reviews.router)     # /reviews/*
app.include_router(messages.router)    # /messages/*
app.include_router(ai.router)          # /ai/*
app.include_router(agencies.router)    # /agencies/*
app.include_router(search.router)      # /search/*

@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}