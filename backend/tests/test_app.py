from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_dashboard():
    r = client.get("/api/dashboard")
    assert r.status_code == 200
    assert "properties" in r.json()

def test_create_property_and_investor():
    p = client.post("/api/properties", json={
        "address":"123 Main St","city":"Cleveland","state":"Ohio",
        "property_type":"Single Family","asking_price":120000,"source":"Test"
    })
    assert p.status_code == 200
    i = client.post("/api/investors", json={
        "name":"Test Investor","location":"Cleveland, Ohio",
        "property_types":"Single Family","min_price":80000,"max_price":150000,
        "strategies":"Fix & Flip","cash_buyer":True
    })
    assert i.status_code == 200
    r = client.post("/api/matches/generate")
    assert r.status_code == 200
