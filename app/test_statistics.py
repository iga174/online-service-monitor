from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.database_models import Base, ServiceCheckDB
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

def test_get_statistics():
    clean_database()
    created_response = client.post("/services", json={"name": "Test Service", "url": "https://example.com"})

    service_id = created_response.json()["id"]
    db = SessionLocal()

    # Daten anlegen

    db.add(ServiceCheckDB(service_id = service_id, 
                               reachable = True,
                               status_code = 200,
                               response_time = 1.5))
    db.add(ServiceCheckDB(service_id = service_id, 
                                   reachable = True,
                                   status_code = 200,
                                   response_time = 0.5))
    db.add(ServiceCheckDB(service_id = service_id, 
                                   reachable = True,
                                   status_code = 200,
                                   response_time = 1.0))

    db.commit()
    db.close()

    # Statistiken abrufen
    response = client.get(f"/services/{service_id}/statistics")

    assert response.status_code == 200
    assert response.json()["average_response_time"] == 1.0
    assert response.json()["min_response_time"] == 0.5
    assert response.json()["max_response_time"] == 1.5
    assert response.json()["total_checks"] == 3
    assert response.json()["successful_checks"] == 3
    assert response.json()["failed_checks"] == 0
    assert response.json()["availability"] == 100