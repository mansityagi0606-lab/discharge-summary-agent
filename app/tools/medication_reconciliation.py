class MedicationReconciliationTool:

    def run(
        self,
        admission_meds,
        discharge_meds,
        raw_text=""
    ):

        changes = []

        admission_names = {
            med["name"].lower()
            for med in admission_meds
            if isinstance(med, dict)
            and med.get("name")
        }

        discharge_names = {
            med["name"].lower()
            for med in discharge_meds
            if isinstance(med, dict)
            and med.get("name")
        }

        # --------------------------------
        # Standard reconciliation
        # --------------------------------

        added = discharge_names - admission_names

        stopped = admission_names - discharge_names

        for med in added:

            changes.append(
                {
                    "type": "ADDED",
                    "medication": med,
                    "reason":
                    "DOCUMENTED_REASON_MISSING"
                }
            )

        for med in stopped:

            changes.append(
                {
                    "type": "STOPPED",
                    "medication": med,
                    "reason":
                    "DOCUMENTED_REASON_MISSING"
                }
            )

        # --------------------------------
        # Safety checks from history
        # --------------------------------

        text = raw_text.lower()

        # Thyroid history
        if (
            "thyroid disorder" in text
            or "thyroid" in text
        ):

            thyroid_found = False

            thyroid_keywords = [
                "thyronorm",
                "eltroxin",
                "levothyroxine",
                "thyroxine"
            ]

            for med in discharge_names:

                for keyword in thyroid_keywords:

                    if keyword in med:

                        thyroid_found = True
                        break

            if not thyroid_found:

                changes.append(
                    {
                        "type":
                        "REVIEW_REQUIRED",
                        "message":
                        (
                            "History indicates thyroid "
                            "treatment but no thyroid "
                            "medication identified in "
                            "discharge medications."
                        )
                    }
                )

        return changes