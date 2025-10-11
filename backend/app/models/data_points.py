"""
Data Points Model - Normalized Storage Layer

This is the "source of truth" for all extracted financial data.
Each data point represents a single financial transaction/entry with:
- Full lineage (which file, which row/page)
- Conflict resolution metadata
- Manual correction capability
- Version history
"""

from sqlalchemy import Column, String, Float, DateTime, Integer, Text, Boolean, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.database import Base


class DataPointType(str, enum.Enum):
    """Types of financial data points."""
    TRANSACTION = "transaction"  # Invoice, receipt, payment
    BUDGET_ITEM = "budget_item"  # Budget line item
    CONTRACT = "contract"  # Contract value
    CHANGE_ORDER = "change_order"  # Contract change
    PAYMENT = "payment"  # Payment record
    COST = "cost"  # Direct cost entry
    REVENUE = "revenue"  # Revenue entry


class DataPointStatus(str, enum.Enum):
    """Processing status of data point."""
    EXTRACTED = "extracted"  # Just extracted from file
    VALIDATED = "validated"  # Passed validation rules
    CONFLICTED = "conflicted"  # Conflict detected with another data point
    MANUALLY_CORRECTED = "manually_corrected"  # Human edited
    APPROVED = "approved"  # Ready for processing


class DataPoint(Base):
    """
    Normalized storage for all financial data points.

    This table is the single source of truth for all extracted data.
    Each row represents one financial transaction/entry with full lineage.
    """
    __tablename__ = "data_points"

    # Primary key
    id = Column(String, primary_key=True, index=True)

    # Project identification
    project_id = Column(String, nullable=False, index=True)

    # Source file lineage
    source_file_id = Column(String, nullable=False, index=True)  # FK to extracted_data
    source_file_name = Column(String, nullable=False)
    source_file_type = Column(String)  # pdf, xlsx, csv
    source_location = Column(String)  # Page 3, Row 15, Cell B7, etc.

    # Data point classification
    data_point_type = Column(SQLEnum(DataPointType), nullable=False, index=True)
    status = Column(SQLEnum(DataPointStatus), default=DataPointStatus.EXTRACTED, index=True)

    # Financial data (normalized schema)
    transaction_date = Column(DateTime, nullable=True)
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    vendor = Column(String, nullable=True)
    category = Column(String, nullable=True)  # After categorization

    # Additional fields for specific types
    invoice_number = Column(String, nullable=True)
    po_number = Column(String, nullable=True)
    cost_code = Column(String, nullable=True)
    gl_account = Column(String, nullable=True)

    # Conflict resolution
    conflict_group_id = Column(String, nullable=True, index=True)  # Group conflicting data points
    is_duplicate = Column(Boolean, default=False)
    superseded_by = Column(String, nullable=True)  # ID of data point that replaced this
    confidence_score = Column(Float, default=1.0)  # Extraction confidence

    # Manual corrections
    manually_edited = Column(Boolean, default=False)
    edited_by = Column(String, nullable=True)
    edit_reason = Column(Text, nullable=True)
    original_values = Column(Text, nullable=True)  # JSON of original values before edit

    # Metadata
    extraction_method = Column(String)  # mineru, pandas, manual_upload
    raw_text = Column(Text, nullable=True)  # Original extracted text
    structured_metadata = Column(Text, nullable=True)  # JSON with additional fields

    # Timestamps
    extracted_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    processed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<DataPoint {self.id} [{self.data_point_type}] {self.description[:30]} ${self.amount}>"


class DataPointConflict(Base):
    """
    Tracks conflicts between data points.

    When multiple files contain different values for the same transaction,
    this table stores the conflict for manual resolution.
    """
    __tablename__ = "data_point_conflicts"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, nullable=False, index=True)
    conflict_group_id = Column(String, nullable=False, index=True)

    # Conflicting data points
    data_point_ids = Column(Text, nullable=False)  # JSON array of IDs

    # Conflict details
    conflict_type = Column(String, nullable=False)  # amount_mismatch, duplicate, date_conflict
    conflict_description = Column(Text)
    suggested_resolution = Column(String)  # keep_first, keep_last, merge, manual_review

    # Resolution
    resolved = Column(Boolean, default=False, index=True)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(String, nullable=True)
    resolution_action = Column(String, nullable=True)  # Which action was taken
    winning_data_point_id = Column(String, nullable=True)  # Which data point was kept

    # Timestamps
    detected_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<DataPointConflict {self.id} [{self.conflict_type}] {self.data_point_ids}>"


class DataPointValidationRule(Base):
    """
    Validation rules for data points.

    Defines business rules that data points must satisfy.
    """
    __tablename__ = "data_point_validation_rules"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, nullable=True)  # NULL = applies to all projects

    # Rule definition
    rule_name = Column(String, nullable=False)
    rule_type = Column(String, nullable=False)  # range_check, format_check, cross_reference
    data_point_type = Column(SQLEnum(DataPointType), nullable=True)  # NULL = applies to all

    # Rule parameters (JSON)
    rule_parameters = Column(Text, nullable=False)  # {"min_amount": 0, "max_amount": 1000000}
    error_message = Column(Text)
    severity = Column(String, default="warning")  # error, warning, info

    # Status
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<ValidationRule {self.rule_name} [{self.severity}]>"
