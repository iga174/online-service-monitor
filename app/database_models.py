from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from datetime import datetime, UTC

Base = declarative_base()

class Service(Base):

    __tablename__ = "service"

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

class ServiceCheckDB(Base):

    __tablename__ = "service_check"

    id = Column(Integer, primary_key = True, index = True)
    service_id = Column(Integer, ForeignKey("service.id"), nullable=False)
    checked_at = Column(DateTime, default=lambda: datetime.now(UTC))
    reachable = Column(Boolean) 
    status_code = Column(Integer) 
    response_time = Column(Float)