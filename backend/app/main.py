"""
FastAPI Backend for Intelligent Finance Platform
Processes Excel files and provides REST API for React dashboard
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import projects, uploads, auth, documents, financials, extraction, aggregation, batch, email, webhooks, system, automation, templates, folder_watch, extraction_test, project_files, financial_builder
from app.middleware import setup_error_handling


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle (startup/shutdown).
    """
    # Startup
    print("🚀 Starting Intelligent Finance Platform...")

    # Initialize database
    from app.database import init_db
    init_db()

    # Validate configuration
    from app.config import validate_config
    config = validate_config()
    print(f"✅ Configuration validated (environment: {config.environment})")

    # Start batch scheduler
    from batch.scheduler import get_scheduler
    scheduler = get_scheduler()
    scheduler.start()
    print("✅ Batch scheduler started")

    print("🎉 Application startup complete")

    yield

    # Shutdown
    print("🛑 Shutting down Intelligent Finance Platform...")

    from batch.scheduler import shutdown_scheduler
    shutdown_scheduler()
    print("✅ Batch scheduler stopped")

    print("👋 Application shutdown complete")


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
allowed_origins = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:5174",  # Vite alternate port
    "http://localhost:3000",  # Alternative dev port
    "https://intelligent-finance-platform.vercel.app",  # Vercel production
    "https://intelligent-finance-platform-git-main-hussein-srours-projects.vercel.app",  # Vercel preview
]

# Add custom frontend URL from environment variable if set
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url and frontend_url not in allowed_origins:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
app.include_router(email.router)  # Email integration for automated uploads
app.include_router(webhooks.router)  # Cloud storage webhooks (Dropbox, Google Drive, OneDrive)
app.include_router(automation.router)  # Automated file processing pipeline
app.include_router(system.router)  # System health, monitoring, and configuration
app.include_router(templates.router)  # Excel template population
app.include_router(folder_watch.router)  # Local folder monitoring
app.include_router(extraction_test.router)  # MinerU extraction testing and comparison
app.include_router(project_files.router)  # Project file structure for AI animation
app.include_router(financial_builder.router)  # Financial Builder - full pipeline processing


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
