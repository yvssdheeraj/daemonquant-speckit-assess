from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Quant Research Brain API"}

def test_create_and_read_strategy():
    response = client.post(
        "/strategies/",
        json={"name": "Test Strategy", "description": "A test strategy"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Strategy"
    assert "id" in data

    strategy_id = data["id"]
    response = client.get(f"/strategies/{strategy_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == strategy_id
    assert data["name"] == "Test Strategy"
