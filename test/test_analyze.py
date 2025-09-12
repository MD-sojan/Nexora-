import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_analyze_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/analyze/",
            json={"content": "Check IP 8.8.8.8 and domain evil.com", "ioc_scan": True}
        )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "risks" in data
    assert "recommendations" in data
    assert any(ioc["type"] == "ipv4" for ioc in data.get("iocs", []))
