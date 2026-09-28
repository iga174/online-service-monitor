from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.database_models import Base
from app.database import get_db

test_db_url = "sqlite:///:memory:"

engine = create_engine(test_db_url, connect_args={"check_same_thread": False}, poolclass=StaticPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    test_db = SessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()

app.dependency_overrides[get_db] = override_get_db

def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_add_service():
    clean_database()
    response = client.post("/services", json={"name": "Test Service", "url": "https://example.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Service"
    assert response.json()["url"] == "https://example.com"

def test_get_service():
    clean_database()
    created_response = client.post("/services",json={"name": "Test Service", "url": "https://example.com"})
    
    service_id = created_response.json()["id"]
    response = client.get(f"/service/{service_id}")

    assert response.status_code == 200
    assert response.json()["id"] == service_id
    assert response.json()["name"] == "Test Service"
    assert response.json()["url"] == "https://example.com"
    
    
def test_update_service():
    clean_database()
    created_response = client.post("/services",json={"name": "Test Service", "url": "https://example.com"})

    service_id = created_response.json()["id"]

    response = client.patch(f"/services/{service_id}",
        json={"name": "Updated Service","url": "https://example.org"})

    assert response.status_code == 200
    assert response.json()["id"] == service_id
    assert response.json()["name"] == "Updated Service"
    assert response.json()["url"] == "https://example.org"

def test_delete_service():
    clean_database()
    created_response = client.post("/services",json={"name": "Test Service", "url": "https://example.com"})
    
    service_id = created_response.json()["id"]
    
    response = client.delete(f"/services/{service_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Service deleted successfully"

    get_response = client.get(f"/service/{service_id}")

    assert get_response.status_code == 404