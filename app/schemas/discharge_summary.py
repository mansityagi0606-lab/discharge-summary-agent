from pydantic import BaseModel, Field
from typing import List, Optional


class Diagnosis(BaseModel):
    principal: Optional[str] = None
    secondary: List[str] = Field(default_factory=list)


class MedicationData(BaseModel):
    admission_meds: List[str] = Field(default_factory=list)
    discharge_meds: List[str] = Field(default_factory=list)


class PendingResults(BaseModel):
    pending_results: List[str] = Field(default_factory=list)