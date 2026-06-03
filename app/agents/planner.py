class Planner:

    def decide_next_action(self, state):

        if not state.diagnoses:
            return "extract_diagnosis"

        if not state.discharge_medications:
            return "extract_medications"

        if not state.medication_reconciliation_done:
            return "reconcile_medications"

        return "generate_summary"