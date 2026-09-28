from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from app.database_models import Service
from app.schemas import ServiceCreate
from app import database_models
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/")
def index(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return services
    
@router.get("/service/{id}")
def get_service(id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == id).first()
    if service == None:
        raise HTTPException(status_code=404, detail="Service not found")

    return service

@router.post("/services")
def add_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = database_models.Service(name=service.name, url=service.url)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.patch("/services/{id}")
def update_service(id: int, service_update: ServiceCreate, db: Session = Depends(get_db)):

    service = db.query(Service).filter(Service.id == id).first()
    if service == None:
        raise HTTPException(status_code=404, detail="Service not found")
        
    service.name = service_update.name
    service.url = service_update.url

    db.commit()
    db.refresh(service)

    return service


@router.delete("/services/{id}")
def delete_service(id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == id).first() 
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()
    return {"message": "Service deleted successfully"}