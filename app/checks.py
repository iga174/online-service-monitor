import threading, schedule, httpx, time
from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db, SessionLocal
from app.database_models import Service, ServiceCheckDB
from sqlalchemy.orm import Session

router = APIRouter()

# helper function for measure_response_time(id)
def check_service(service, db):
    start = time.perf_counter()
    # call website
    try:
        response = httpx.get(service.url, timeout=5)
    
    except httpx.TimeoutException:
        db_service = ServiceCheckDB(service_id=service.id, reachable = False, status_code=None, response_time=None)
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        return db_service
        
    except httpx.ConnectError:
        db_service = ServiceCheckDB(service_id=service.id, reachable = False, status_code=None, response_time=None)
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        return db_service
                    
                
    except httpx.RequestError:
        db_service = ServiceCheckDB(service_id=service.id, reachable = False, status_code=None, response_time=None)
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        return db_service
                    
                
    end = time.perf_counter()
        
    response_time = end - start
        
    db_service = ServiceCheckDB(service_id=service.id, reachable = True, status_code=response.status_code, response_time=response_time)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
                
    return db_service
    

@router.post("/services/{id}/check")
def measure_response_time(id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return check_service(service, db)

@router.get("/services/{id}/checks")
def get_checks(id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
            
    checks = db.query(ServiceCheckDB).filter(ServiceCheckDB.service_id == id).all()
    return checks

def check_all_services():
    db = SessionLocal()
    try:
        services = db.query(Service).all()

        for service in services:
            check_service(service, db)
    finally:
        db.close()
            
# run check_all_services() every 60s
schedule.every(60).seconds.do(check_all_services)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# run the scheduler in a seperate thread (so it doesn't block the FastAPI app)
scheduler_thread = threading.Thread(target=run_scheduler,daemon=True)

scheduler_thread.start()
