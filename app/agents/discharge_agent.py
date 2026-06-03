from app.agents.planner import Planner

from app.tools.diagnosis_extractor import DiagnosisExtractor
from app.tools.medication_extractor import MedicationExtractor
from app.tools.medication_reconciliation import (
    MedicationReconciliationTool,
)
from app.tools.conflict_checker import ConflictChecker
from app.tools.drug_interaction_tool import (
    DrugInteractionTool,
)
from app.tools.clinician_review_tool import (
    ClinicianReviewTool,
)
from app.tools.structured_medication_extractor import (
    StructuredMedicationExtractor
)

from app.utils.trace_logger import TraceLogger


class DischargeAgent:

    MAX_STEPS = 10

    def __init__(self, state):

        self.state = state

        self.planner = Planner()

        self.trace = TraceLogger()

        self.diagnosis_tool = DiagnosisExtractor()

        self.medication_tool = MedicationExtractor()

        self.reconciliation_tool = (
            MedicationReconciliationTool()
        )

        self.conflict_checker = ConflictChecker()

        self.interaction_tool = (
            DrugInteractionTool()
        )

        self.review_tool = (
            ClinicianReviewTool()
        )

        self.structured_med_tool = (
            StructuredMedicationExtractor()
        )

    def run(self):

        while (
            self.state.step_count < self.MAX_STEPS
            and not self.state.completed
        ):

            action = self.planner.decide_next_action(
                self.state
            )

            self.state.step_count += 1

            try:

                # -------------------------
                # Extract Diagnoses
                # -------------------------
                if action == "extract_diagnosis":

                    diagnoses = self.diagnosis_tool.run(
                        self.state.raw_text
                    )

                    self.state.diagnosis_evidence = diagnoses

                    self.state.diagnoses = [
                        item["value"]
                        for item in diagnoses
                    ]

                    self.trace.add(
                        reasoning="Need diagnoses before generating summary",
                        tool="DiagnosisExtractor",
                        tool_input="raw_text",
                        result=str(diagnoses),
                        next_action="re-plan",
                    )

                # -------------------------
                # Extract Medications
                # -------------------------
                elif action == "extract_medications":

                    meds = self.medication_tool.run(
                        self.state.raw_text
                    )

                    self.state.discharge_medications = meds
                    structured = (
                                self.structured_med_tool.run(
                                self.state.raw_text
                            )
                    )

                    self.state.structured_medications = (
                    structured
                    )

                    self.trace.add(
                        reasoning="Need discharge medications",
                        tool="MedicationExtractor",
                        tool_input="raw_text",
                        result=f"{len(meds)} medications extracted",
                        next_action="re-plan",
                    )

                # -------------------------
                # Reconcile Medications
                # -------------------------
                elif action == "reconcile_medications":

                    changes = (
                        self.reconciliation_tool.run(
                            self.state.admission_medications,
                            self.state.discharge_medications,
                            self.state.raw_text
                        )
                    )

                    self.state.medication_changes = (
                        changes
                    )

                    self.state.medication_reconciliation_done = (
                        True
                    )

                    self.trace.add(
                        reasoning="Need medication reconciliation",
                        tool="MedicationReconciliationTool",
                        tool_input="admission vs discharge meds",
                        result=str(changes),
                        next_action="re-plan",
                    )

                # -------------------------
                # Generate Summary
                # -------------------------
                elif action == "generate_summary":

                    self._detect_pending_items()

                    self._detect_missing_fields()

                    self._check_conflicts()

                    self._check_drug_interactions()

                    self._generate_summary()

                    self.state.completed = True

                    self.trace.add(
                        reasoning="All required information gathered",
                        tool="SummaryGenerator",
                        tool_input="state",
                        result="summary draft generated",
                        next_action="finish",
                    )

                # -------------------------
                # Finish
                # -------------------------
                elif action == "finish":

                    self.state.completed = True

            except Exception as e:

                error_message = (
                    f"Tool failure: {str(e)}"
                )

                self.state.safety_flags.append(
                    error_message
                )

                self.trace.add(
                    reasoning="Tool execution failed",
                    tool=action,
                    tool_input="N/A",
                    result=str(e),
                    next_action="continue",
                )

        self.trace.export()

        return self.state

    # ==========================================
    # Helper Methods
    # ==========================================

    def _detect_pending_items(self):

        text = self.state.raw_text.lower()

        if "report awaited" in text:

            self.state.pending_items.append(
                "Urine culture and sensitivity report awaited"
            )

        if "awaited" in text:

            if (
                "One or more reports pending"
                not in self.state.pending_items
            ):
                self.state.pending_items.append(
                    "One or more reports pending"
                )

    def _detect_missing_fields(self):

        if not self.state.diagnoses:

            self.state.missing_fields.append(
                "Diagnosis"
            )

        if not self.state.discharge_medications:

            self.state.missing_fields.append(
                "Discharge Medications"
            )

    def _check_conflicts(self):

        conflicts = self.conflict_checker.run(
            self.state
        )

        self.state.conflicts.extend(
            conflicts
        )

    def _check_drug_interactions(self):

        medication_names = []

        for med in self.state.discharge_medications:

            if isinstance(med, dict):

                if med.get("name"):

                    medication_names.append(
                        med["name"]
                    )

        if not medication_names:
            return

        interactions = (
            self.interaction_tool.run(
                medication_names
            )
        )

        if interactions:

            for interaction in interactions:

                self.state.safety_flags.append(
                    f"Drug Interaction: {interaction}"
                )

                review_result = (
                    self.review_tool.run(
                        f"Drug interaction found: {interaction}"
                    )
                )

                self.state.safety_flags.append(
                    str(review_result)
                )

    def _generate_summary(self):

      summary = []

      summary.append(
        "===== DISCHARGE SUMMARY DRAFT ====="
        )

      summary.append("")

    # -------------------------
    # Diagnoses
    # -------------------------

      summary.append("Diagnoses:")

      if self.state.diagnosis_evidence:
          for diagnosis in self.state.diagnosis_evidence:

            summary.append(
                f"- {diagnosis.get('value', 'UNKNOWN')}"
            )

            summary.append(
                f"  Evidence: {diagnosis.get('evidence', 'Not Available')}"
            )

      else:
          summary.append(
            "- MISSING (Clinician Review Required)"
          )

      summary.append("")

    # -------------------------
    # Discharge Medications
    # -------------------------

      summary.append(
        "Discharge Medications:"
       )

      if self.state.structured_medications:
          for med in self.state.structured_medications:

            summary.append(
                f"- {med.get('name') or 'UNKNOWN MEDICATION'}"
            )

            summary.append(
                f"  Frequency: {med.get('frequency') or 'Not documented'}"
            )

            summary.append(
                f"  Duration: {med.get('duration') or 'Not documented'}"
            )

            summary.append(
                f"  Evidence: {med.get('evidence') or 'Not available'}"
            )

      else:
          summary.append(
            "- No medications extracted"
          )

      summary.append("")

    # -------------------------
    # Pending Results
    # -------------------------

      summary.append(
        "Pending Results:"
        )

      if self.state.pending_items:
          for item in self.state.pending_items:
              summary.append(
                f"- {item}"
              )

      else:
          summary.append(
            "- None documented"
          )

      summary.append("")

    # -------------------------
    # Medication Reconciliation
    # -------------------------

      summary.append(
        "Medication Reconciliation:"
       )

      if self.state.medication_changes:
          for change in self.state.medication_changes:
              if change.get("type") == "REVIEW_REQUIRED":
                  summary.append(
                    f"- REVIEW REQUIRED: "
                    f"{change.get('message')}"
                )

      else:
        summary.append(
            f"- {change.get('type')}: "
            f"{change.get('medication')}"
        )

        summary.append(
            f"  Reason: "
            f"{change.get('reason')}"
        )

      summary.append("")

    # -------------------------
    # Conflicts
    # -------------------------

      summary.append("Conflicts:")

      if self.state.conflicts:
          for conflict in self.state.conflicts:
              summary.append(
                f"- {conflict}"
                )

      else:
          summary.append(
            "- None detected"
            )

      summary.append("")

    # -------------------------
    # Missing Fields
    # -------------------------

      summary.append(
        "Missing Fields:"
       )

      if self.state.missing_fields:
          for field in self.state.missing_fields:
              summary.append(
                f"- {field}"
            )

      else:
          summary.append(
            "- None"
           )

      summary.append("")

    # -------------------------
    # Safety Flags
    # -------------------------

      summary.append(
        "Safety Flags:"
       )

      if self.state.safety_flags:
          for flag in self.state.safety_flags:
              summary.append(
                f"- {flag}"
            )

      else:
          summary.append(
            "- None"
        )

      self.state.summary_draft = "\n".join(summary)