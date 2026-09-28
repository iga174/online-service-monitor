from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

# Database connection URL
db_url = "sqlite:///./service_monitor.db"

engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()