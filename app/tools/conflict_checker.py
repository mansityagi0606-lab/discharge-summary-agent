import re


class ConflictChecker:

    def run(self, state):

        conflicts = []

        text = state.raw_text

        # ---------------------------------
        # Duplicate diagnoses
        # ---------------------------------

        diagnosis_set = set()

        for diagnosis in state.diagnoses:

            normalized = (
                diagnosis.strip()
                .lower()
            )

            if normalized in diagnosis_set:

                conflicts.append(
                    f"Duplicate diagnosis detected: {diagnosis}"
                )

            diagnosis_set.add(
                normalized
            )

        # ---------------------------------
        # Multiple diagnosis sections
        # ---------------------------------

        diagnosis_sections = re.findall(
            r"DIAGNOSIS:(.*?)(?:HISTORY:|$)",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        if len(diagnosis_sections) > 1:

            conflicts.append(
                "Multiple diagnosis sections found. Clinician review required."
            )

        # ---------------------------------
        # Discharge status contradictions
        # ---------------------------------

        stable = (
            "hemodynamically stable"
            in text.lower()
        )

        unstable_terms = [
            "critical",
            "unstable",
            "icu transfer",
            "shock"
        ]

        unstable_found = any(
            term in text.lower()
            for term in unstable_terms
        )

        if stable and unstable_found:

            conflicts.append(
                "Conflicting discharge condition documented."
            )

        # ---------------------------------
        # Pending + completed conflict
        # ---------------------------------

        if (
            "report awaited"
            in text.lower()
            and
            "normal report"
            in text.lower()
        ):

            conflicts.append(
                "Report appears both completed and pending."
            )

        # ---------------------------------
        # Medication instruction conflicts
        # ---------------------------------

        medication_names = []

        for med in getattr(
            state,
            "structured_medications",
            []
        ):

            name = med.get("name")

            if name:

                medication_names.append(
                    name.lower()
                )

        duplicates = set()

        for med in medication_names:

            if medication_names.count(med) > 1:

                duplicates.add(
                    med
                )

        for med in duplicates:

            conflicts.append(
                f"Medication appears multiple times: {med}"
            )

        return conflicts