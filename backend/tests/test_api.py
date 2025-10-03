"""
API Integration Tests

Tests key API endpoints to ensure they're working correctly.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    """Create test client"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "version" in data


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test health check endpoint"""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_system_health_endpoint(client):
    """Test system health monitoring endpoint"""
    response = await client.get("/api/system/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "system_resources" in data
    assert "platform" in data


@pytest.mark.asyncio
async def test_authentication_required(client):
    """Test that protected endpoints require authentication"""
    # These endpoints should return 401 without auth
    protected_endpoints = [
        "/api/projects/dashboard",
        "/api/templates/list",
        "/api/folder-watch/status"
    ]

    for endpoint in protected_endpoints:
        response = await client.get(endpoint)
        assert response.status_code == 401, f"Expected 401 for {endpoint}, got {response.status_code}"


@pytest.mark.asyncio
async def test_templates_list_unauthorized(client):
    """Test that template list requires authentication"""
    response = await client.get("/api/templates/list")
    assert response.status_code == 401
