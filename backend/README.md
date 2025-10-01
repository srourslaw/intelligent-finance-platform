# Intelligent Finance Platform - Backend API

FastAPI backend that processes construction project Excel files and provides REST API endpoints for the React dashboard.

## Running the Server

```bash
cd backend
python3 -m uvicorn app.main:app --reload --port 8000
```

API Documentation: http://localhost:8000/docs

## API Endpoints

- GET /api/projects/health - Check health
- GET /api/projects/dashboard - Complete dashboard data
- GET /api/projects/budget - Budget data
- GET /api/projects/subcontractors - Subcontractor data
- GET /api/projects/client-payments - Client payments
- GET /api/projects/defects - Defects list
