import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/chat/", json={"message": "Hello Nexora"})
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["mock"] is True
