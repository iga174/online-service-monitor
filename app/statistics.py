from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from app.database_models import Service, ServiceCheckDB
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/services/{id}/statistics")
def get_statistics(id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == id).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    checks = db.query(ServiceCheckDB).filter(
        ServiceCheckDB.service_id == id
    ).all()

    response_times = []

    for check in checks:
        if check.response_time is not None:
            response_times.append(check.response_time)

    if len(response_times) == 0:
        average = None
        minimum = None
        maximum = None
        total_checks = len(checks)
        successful_checks = 0
        failed_checks = total_checks
        availability = 0.0

    else:
        average = sum(response_times) / len(response_times)
        minimum = min(response_times)
        maximum = max(response_times)

        successful_checks = len(response_times)
        total_checks = len(checks)
        failed_checks = total_checks - successful_checks

        availability = (successful_checks / total_checks) * 100

    return {
        "average_response_time": average,
        "min_response_time": minimum,
        "max_response_time": maximum,
        "total_checks": total_checks,
        "successful_checks": successful_checks,
        "failed_checks": failed_checks,
        "availability": availability
    }

    