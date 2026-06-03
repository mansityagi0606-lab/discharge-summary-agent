from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class AgentState:

    # Raw OCR text
    raw_text: str = ""

    # Extracted diagnoses (plain text)
    diagnoses: List[str] = field(
        default_factory=list
    )

    # Diagnosis + evidence
    diagnosis_evidence: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Structured medications
    structured_medications: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Admission medications
    admission_medications: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Discharge medications
    discharge_medications: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Medication reconciliation results
    medication_changes: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Prevent reconciliation loop
    medication_reconciliation_done: bool = False

    # Missing information
    missing_fields: List[str] = field(
        default_factory=list
    )

    # Pending reports/labs
    pending_items: List[str] = field(
        default_factory=list
    )

    # Conflicting information
    conflicts: List[str] = field(
        default_factory=list
    )

    # Safety concerns
    safety_flags: List[str] = field(
        default_factory=list
    )

    # Final generated summary
    summary_draft: str = ""

    # Agent execution trace
    trace: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Agent loop control
    step_count: int = 0

    completed: bool = False