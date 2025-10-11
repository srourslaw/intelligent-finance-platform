"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Database file path
DB_PATH = Path(__file__).parent.parent / "data" / "financial_builder.db"
DB_PATH.parent.mkdir(exist_ok=True)

# SQLite database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.
    Creates all tables defined in models.
    """
    # Import models to register them
    from app.models.extraction import ExtractionJob, ExtractedData, Transaction
    from app.models.data_points import DataPoint, DataPointConflict, DataPointValidationRule

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized at {DB_PATH}")
