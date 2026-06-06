"""
Restaurant Orders API - Main Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time

from app.routers import orders, menu, payments
from app.database import engine, Base

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Orders API",
    description=(
        "A RESTful API to manage restaurant orders, menu items, and payments. "
        "Provides full order details including items, prices, and payment breakdowns."
    ),
    version="1.0.0",
    contact={
        "name": "Indrajit Mandol",
        "url": "https://indrajit-mandoll.netlify.app",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Security Middlewares ────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["GET"],        # Read-only API
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],          # Restrict in production
)

# ── Request Timing Middleware ───────────────────────────────────────────────

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{(time.time() - start) * 1000:.2f}ms"
    return response

# ── Routers ─────────────────────────────────────────────────────────────────

app.include_router(orders.router,   prefix="/api/v1", tags=["Orders"])
app.include_router(menu.router,     prefix="/api/v1", tags=["Menu"])
app.include_router(payments.router, prefix="/api/v1", tags=["Payments"])

# ── Root ─────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Restaurant Orders API is running", "version": "1.0.0"}
