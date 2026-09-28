from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.database_models import Base, Service, ServiceCheckDB


test_db_url = "sqlite:///:memory:"

engine = create_engine(
    test_db_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_measure_response_time():
    clean_database()
    created_response = client.post("/services",json={"name": "Test Service", "url": "https://example.com"})

    service_id = created_response.json()["id"]
    
    response = client.post(f"/services/{service_id}/check")

    assert response.json()["service_id"] == service_id
    assert response.json()["reachable"] is True
    assert response.json()["status_code"] == 200
    assert response.json()["response_time"] is not None
    assert response.json()["response_time"] > 0

def test_get_checks():
    clean_database()

    created_response = client.post("/services",json={"name": "Test Service","url": "https://example.com"})

    assert created_response.status_code == 200

    service_id = created_response.json()["id"]

    client.post(f"/services/{service_id}/check")
    client.post(f"/services/{service_id}/check")
    client.post(f"/services/{service_id}/check")

    # Checks abrufen
    response = client.get(f"/services/{service_id}/checks")

    assert response.status_code == 200

    checks = response.json()

    assert len(checks) == 3

    for check in checks:
        assert check["service_id"] == service_id
        assert check["reachable"] is True
        assert check["status_code"] == 200
        assert check["response_time"] is not None
        assert check["response_time"] > 0