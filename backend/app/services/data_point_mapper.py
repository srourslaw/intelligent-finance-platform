"""
Data Point Mapping Service

Handles:
- Deduplication of data points
- Conflict detection and resolution
- Manual correction tracking
- Data point validation
"""

import logging
import uuid
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.data_points import (
    DataPoint, DataPointConflict, DataPointStatus,
    DataPointType, DataPointValidationRule
)

logger = logging.getLogger(__name__)


class DataPointMapper:
    """Service for mapping, deduplicating, and validating data points."""

    def __init__(self, db: Session, project_id: str):
        self.db = db
        self.project_id = project_id

    def process_data_points(
        self,
        data_points: List[DataPoint]
    ) -> Tuple[List[DataPoint], List[DataPointConflict]]:
        """
        Process data points: deduplicate, detect conflicts, validate.

        Returns:
            Tuple of (processed_data_points, conflicts)
        """
        logger.info(f"Processing {len(data_points)} data points for project {self.project_id}")

        # Save all data points first
        processed_points = []
        conflicts = []

        for dp in data_points:
            # Check for duplicates
            duplicate_check = self._check_duplicate(dp)

            if duplicate_check:
                # Found potential duplicate
                is_exact_duplicate, existing_dp = duplicate_check

                if is_exact_duplicate:
                    # Mark as duplicate, don't save
                    logger.info(f"Skipping exact duplicate: {dp.description[:50]}")
                    dp.is_duplicate = True
                    dp.superseded_by = existing_dp.id
                    continue
                else:
                    # Potential conflict - save both and create conflict record
                    conflict = self._create_conflict(dp, existing_dp, 'potential_duplicate')
                    conflicts.append(conflict)
                    dp.conflict_group_id = conflict.conflict_group_id
                    logger.warning(f"Conflict detected: {dp.description[:50]}")

            # Validate data point
            validation_errors = self._validate_data_point(dp)
            if validation_errors:
                logger.warning(f"Validation errors for {dp.id}: {validation_errors}")
                dp.structured_metadata = json.dumps({
                    **(json.loads(dp.structured_metadata) if dp.structured_metadata else {}),
                    'validation_errors': validation_errors
                })

            # Mark as validated if no errors
            if not validation_errors and not dp.conflict_group_id:
                dp.status = DataPointStatus.VALIDATED

            processed_points.append(dp)

        # Bulk save data points
        if processed_points:
            self.db.add_all(processed_points)
            self.db.commit()
            logger.info(f"Saved {len(processed_points)} data points")

        # Save conflicts
        if conflicts:
            self.db.add_all(conflicts)
            self.db.commit()
            logger.info(f"Detected {len(conflicts)} conflicts")

        return processed_points, conflicts

    def _check_duplicate(
        self,
        data_point: DataPoint
    ) -> Optional[Tuple[bool, DataPoint]]:
        """
        Check if data point is duplicate or conflict.

        Returns:
            None if no duplicate found
            (True, existing_dp) if exact duplicate
            (False, existing_dp) if potential conflict
        """
        # Look for similar data points in same project
        # within reasonable time window (±7 days)
        date_window = timedelta(days=7)

        query = self.db.query(DataPoint).filter(
            DataPoint.project_id == self.project_id,
            DataPoint.is_duplicate == False,
            DataPoint.superseded_by == None
        )

        # Add date filter if transaction has date
        if data_point.transaction_date:
            query = query.filter(
                or_(
                    DataPoint.transaction_date == None,
                    and_(
                        DataPoint.transaction_date >= data_point.transaction_date - date_window,
                        DataPoint.transaction_date <= data_point.transaction_date + date_window
                    )
                )
            )

        # Search by similar amount (±1%)
        amount_tolerance = abs(data_point.amount * 0.01)
        query = query.filter(
            DataPoint.amount >= data_point.amount - amount_tolerance,
            DataPoint.amount <= data_point.amount + amount_tolerance
        )

        similar_points = query.all()

        for existing_dp in similar_points:
            # Check for exact match
            if self._is_exact_match(data_point, existing_dp):
                return (True, existing_dp)

            # Check for conflict (similar but different)
            if self._is_conflicting(data_point, existing_dp):
                return (False, existing_dp)

        return None

    def _is_exact_match(self, dp1: DataPoint, dp2: DataPoint) -> bool:
        """Check if two data points are exact duplicates."""
        # Same amount
        if abs(dp1.amount - dp2.amount) > 0.01:
            return False

        # Same or very similar description
        desc1 = dp1.description.lower().strip()
        desc2 = dp2.description.lower().strip()
        if desc1 != desc2:
            # Check similarity (simple approach)
            similarity = self._string_similarity(desc1, desc2)
            if similarity < 0.9:
                return False

        # Same date (if both have dates)
        if dp1.transaction_date and dp2.transaction_date:
            if dp1.transaction_date.date() != dp2.transaction_date.date():
                return False

        # Same vendor (if both have vendors)
        if dp1.vendor and dp2.vendor:
            if dp1.vendor.lower().strip() != dp2.vendor.lower().strip():
                return False

        return True

    def _is_conflicting(self, dp1: DataPoint, dp2: DataPoint) -> bool:
        """Check if two data points are conflicting (similar but not identical)."""
        # Similar amount but not exact
        amount_diff = abs(dp1.amount - dp2.amount)
        if 0.01 < amount_diff < abs(dp1.amount * 0.05):  # 0.01 to 5% difference
            # Similar description
            desc1 = dp1.description.lower().strip()
            desc2 = dp2.description.lower().strip()
            similarity = self._string_similarity(desc1, desc2)
            if similarity > 0.7:
                return True

        return False

    def _string_similarity(self, s1: str, s2: str) -> float:
        """Calculate simple string similarity (0.0 to 1.0)."""
        # Simple approach: count common words
        words1 = set(s1.split())
        words2 = set(s2.split())

        if not words1 or not words2:
            return 0.0

        common = words1.intersection(words2)
        total = words1.union(words2)

        return len(common) / len(total) if total else 0.0

    def _create_conflict(
        self,
        dp1: DataPoint,
        dp2: DataPoint,
        conflict_type: str
    ) -> DataPointConflict:
        """Create a conflict record between two data points."""
        conflict_group_id = str(uuid.uuid4())

        # Determine conflict description and suggestion
        amount_diff = abs(dp1.amount - dp2.amount)

        if conflict_type == 'potential_duplicate':
            description = f"Potential duplicate transaction: ${amount_diff:.2f} difference"
            suggestion = "manual_review"
        else:
            description = f"Conflict: {conflict_type}"
            suggestion = "keep_latest"

        conflict = DataPointConflict(
            id=str(uuid.uuid4()),
            project_id=self.project_id,
            conflict_group_id=conflict_group_id,
            data_point_ids=json.dumps([dp1.id, dp2.id]),
            conflict_type=conflict_type,
            conflict_description=description,
            suggested_resolution=suggestion,
            resolved=False
        )

        return conflict

    def _validate_data_point(self, data_point: DataPoint) -> List[str]:
        """
        Validate data point against business rules.

        Returns:
            List of validation error messages
        """
        errors = []

        # Load validation rules for this project/type
        rules = self.db.query(DataPointValidationRule).filter(
            or_(
                DataPointValidationRule.project_id == self.project_id,
                DataPointValidationRule.project_id == None
            ),
            or_(
                DataPointValidationRule.data_point_type == data_point.data_point_type,
                DataPointValidationRule.data_point_type == None
            ),
            DataPointValidationRule.active == True
        ).all()

        # Apply validation rules
        for rule in rules:
            try:
                params = json.loads(rule.rule_parameters)

                if rule.rule_type == 'range_check':
                    if 'min_amount' in params and data_point.amount < params['min_amount']:
                        errors.append(f"{rule.rule_name}: Amount below minimum (${params['min_amount']})")
                    if 'max_amount' in params and data_point.amount > params['max_amount']:
                        errors.append(f"{rule.rule_name}: Amount exceeds maximum (${params['max_amount']})")

                elif rule.rule_type == 'required_field':
                    field_name = params.get('field_name')
                    if field_name and not getattr(data_point, field_name, None):
                        errors.append(f"{rule.rule_name}: Required field '{field_name}' is missing")

                elif rule.rule_type == 'format_check':
                    field_name = params.get('field_name')
                    pattern = params.get('pattern')
                    if field_name and pattern:
                        import re
                        value = str(getattr(data_point, field_name, ''))
                        if value and not re.match(pattern, value):
                            errors.append(f"{rule.rule_name}: Field '{field_name}' format invalid")

            except Exception as e:
                logger.error(f"Error applying validation rule {rule.id}: {e}")

        # Built-in validations
        if data_point.amount == 0:
            errors.append("Amount cannot be zero")

        if not data_point.description or data_point.description.strip() == '':
            errors.append("Description is required")

        if len(data_point.description) > 500:
            errors.append("Description too long (max 500 characters)")

        return errors

    def get_unresolved_conflicts(self) -> List[DataPointConflict]:
        """Get all unresolved conflicts for this project."""
        return self.db.query(DataPointConflict).filter(
            DataPointConflict.project_id == self.project_id,
            DataPointConflict.resolved == False
        ).all()

    def resolve_conflict(
        self,
        conflict_id: str,
        resolution_action: str,
        winning_data_point_id: Optional[str] = None,
        resolved_by: Optional[str] = None
    ) -> DataPointConflict:
        """
        Resolve a conflict.

        Args:
            conflict_id: Conflict ID
            resolution_action: 'keep_first', 'keep_second', 'keep_both', 'merge'
            winning_data_point_id: ID of data point to keep (for keep_first/keep_second)
            resolved_by: User who resolved the conflict

        Returns:
            Updated conflict record
        """
        conflict = self.db.query(DataPointConflict).filter(
            DataPointConflict.id == conflict_id
        ).first()

        if not conflict:
            raise ValueError(f"Conflict {conflict_id} not found")

        # Get data points
        data_point_ids = json.loads(conflict.data_point_ids)
        data_points = self.db.query(DataPoint).filter(
            DataPoint.id.in_(data_point_ids)
        ).all()

        if resolution_action == 'keep_first':
            # Mark second as superseded
            if len(data_points) >= 2:
                data_points[1].superseded_by = data_points[0].id
                data_points[1].status = DataPointStatus.EXTRACTED
                winning_data_point_id = data_points[0].id

        elif resolution_action == 'keep_second':
            # Mark first as superseded
            if len(data_points) >= 2:
                data_points[0].superseded_by = data_points[1].id
                data_points[0].status = DataPointStatus.EXTRACTED
                winning_data_point_id = data_points[1].id

        elif resolution_action == 'keep_both':
            # Approve both data points
            for dp in data_points:
                dp.status = DataPointStatus.APPROVED
                dp.conflict_group_id = None

        elif resolution_action == 'merge':
            # Merge data points (use winning_data_point_id)
            if winning_data_point_id:
                for dp in data_points:
                    if dp.id != winning_data_point_id:
                        dp.superseded_by = winning_data_point_id

        # Update conflict
        conflict.resolved = True
        conflict.resolved_at = datetime.now()
        conflict.resolved_by = resolved_by
        conflict.resolution_action = resolution_action
        conflict.winning_data_point_id = winning_data_point_id

        self.db.commit()

        logger.info(f"Resolved conflict {conflict_id} with action '{resolution_action}'")
        return conflict

    def manually_correct_data_point(
        self,
        data_point_id: str,
        updates: Dict[str, Any],
        edited_by: str,
        edit_reason: Optional[str] = None
    ) -> DataPoint:
        """
        Manually correct a data point.

        Args:
            data_point_id: Data point ID
            updates: Dictionary of fields to update
            edited_by: User making the correction
            edit_reason: Reason for correction

        Returns:
            Updated data point
        """
        data_point = self.db.query(DataPoint).filter(
            DataPoint.id == data_point_id
        ).first()

        if not data_point:
            raise ValueError(f"Data point {data_point_id} not found")

        # Save original values if first edit
        if not data_point.manually_edited:
            original = {
                'amount': data_point.amount,
                'description': data_point.description,
                'transaction_date': data_point.transaction_date.isoformat() if data_point.transaction_date else None,
                'vendor': data_point.vendor,
                'category': data_point.category
            }
            data_point.original_values = json.dumps(original)

        # Apply updates
        for field, value in updates.items():
            if hasattr(data_point, field):
                setattr(data_point, field, value)

        # Update metadata
        data_point.manually_edited = True
        data_point.edited_by = edited_by
        data_point.edit_reason = edit_reason
        data_point.status = DataPointStatus.MANUALLY_CORRECTED
        data_point.updated_at = datetime.now()

        self.db.commit()

        logger.info(f"Manually corrected data point {data_point_id} by {edited_by}")
        return data_point

    def get_data_points_for_processing(
        self,
        include_statuses: Optional[List[DataPointStatus]] = None
    ) -> List[DataPoint]:
        """
        Get data points ready for processing.

        Args:
            include_statuses: List of statuses to include (default: VALIDATED, MANUALLY_CORRECTED, APPROVED)

        Returns:
            List of data points
        """
        if include_statuses is None:
            include_statuses = [
                DataPointStatus.VALIDATED,
                DataPointStatus.MANUALLY_CORRECTED,
                DataPointStatus.APPROVED
            ]

        data_points = self.db.query(DataPoint).filter(
            DataPoint.project_id == self.project_id,
            DataPoint.status.in_(include_statuses),
            DataPoint.is_duplicate == False,
            DataPoint.superseded_by == None
        ).all()

        logger.info(f"Retrieved {len(data_points)} data points for processing")
        return data_points


def create_data_point_mapper(db: Session, project_id: str) -> DataPointMapper:
    """Factory function to create data point mapper."""
    return DataPointMapper(db, project_id)
