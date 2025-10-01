"""
FastAPI Backend for Intelligent Finance Platform
Processes Excel files and provides REST API for React dashboard
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import projects

# Create FastAPI app
app = FastAPI(
    title="Intelligent Finance Platform API",
    description="Backend API for construction project financial management",
    version="1.0.0"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # Alternative dev port
        "https://intelligent-finance-platform.vercel.app",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router)


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
