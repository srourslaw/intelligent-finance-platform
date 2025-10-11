"""
Database models for file extraction and processing
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ExtractionJob(Base):
    """Tracks bulk extraction jobs"""
    __tablename__ = "extraction_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    project_id = Column(String, index=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    total_files = Column(Integer, default=0)
    processed_files = Column(Integer, default=0)
    failed_files = Column(Integer, default=0)
    progress_percent = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    job_metadata = Column(Text, nullable=True)  # JSON string for pipeline results
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    extracted_data = relationship("ExtractedData", back_populates="job")


class ExtractedData(Base):
    """Stores extracted data from individual files"""
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("extraction_jobs.job_id"))
    project_id = Column(String, index=True)
    file_path = Column(String)
    file_name = Column(String)
    file_type = Column(String)  # 'pdf', 'xlsx', 'csv'
    extraction_method = Column(String)  # 'mineru', 'pdfplumber', 'openpyxl'
    raw_text = Column(Text)
    structured_data = Column(Text)  # JSON string for Excel data
    extraction_status = Column(String)  # 'success', 'failed', 'partial'
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    job = relationship("ExtractionJob", back_populates="extracted_data")
    transactions = relationship("Transaction", back_populates="extracted_file")


class Transaction(Base):
    """Categorized transactions mapped to template"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    extracted_data_id = Column(Integer, ForeignKey("extracted_data.id"))
    project_id = Column(String, index=True)
    description = Column(Text)
    amount = Column(Float)
    date = Column(String, nullable=True)

    # AI Categorization
    mapped_category = Column(String)  # e.g., "income_statement.revenue.gross_sales"
    confidence_score = Column(Float)  # 0.0 to 1.0
    mapping_method = Column(String)  # 'keyword', 'llm', 'manual'
    needs_review = Column(Integer, default=0)  # Boolean flag

    # Metadata
    original_source = Column(String)
    page_number = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    extracted_file = relationship("ExtractedData", back_populates="transactions")
