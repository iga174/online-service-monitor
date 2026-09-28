from fastapi import FastAPI
from app.database import engine
from app.database_models import Base
from app.statistics import router as statistics_router
from app.checks import router as checks_router
from app.services import router as services_router

app = FastAPI()
app.include_router(statistics_router)
app.include_router(checks_router)
app.include_router(services_router)
Base.metadata.create_all(bind=engine)

