"""
FastAPI Backend for Intelligent Finance Platform
Processes Excel files and provides REST API for React dashboard
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import projects, uploads, auth, documents, financials, extraction, aggregation, batch
from app.middleware import setup_error_handling


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle (startup/shutdown).
    """
    # Startup
    from batch.scheduler import get_scheduler
    scheduler = get_scheduler()
    scheduler.start()
    print("✅ Batch scheduler started")

    yield

    # Shutdown
    from batch.scheduler import shutdown_scheduler
    shutdown_scheduler()
    print("✅ Batch scheduler stopped")


# Create FastAPI app
app = FastAPI(
    title="Intelligent Finance Platform API",
    description="Backend API for construction project financial management",
    version="1.0.0",
    lifespan=lifespan
)

# Setup error handling and logging middleware
setup_error_handling(app)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:5174",  # Vite alternate port
        "http://localhost:3000",  # Alternative dev port
        "https://intelligent-finance-platform.vercel.app",  # Vercel production
        "https://intelligent-finance-platform-git-main-hussein-srours-projects.vercel.app",  # Vercel preview
        "https://*.vercel.app",  # All Vercel previews
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)  # Auth endpoints (no protection needed)
app.include_router(projects.router)
app.include_router(uploads.router)
app.include_router(documents.router)
app.include_router(financials.router)  # AI-consolidated financial data
app.include_router(extraction.router)  # File extraction and AI classification
app.include_router(aggregation.router)  # Aggregation and validation
app.include_router(batch.router)  # Batch processing and scheduling


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Intelligent Finance Platform API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "health": "/api/projects/health",
            "dashboard": "/api/projects/dashboard",
            "budget": "/api/projects/budget",
            "subcontractors": "/api/projects/subcontractors",
            "client_payments": "/api/projects/client-payments",
            "defects": "/api/projects/defects"
        }
    }


@app.get("/api/health")
async def api_health():
    """API health check"""
    return {
        "status": "healthy",
        "message": "API is running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
