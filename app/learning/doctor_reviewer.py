class DoctorReviewer:

    def review(self, draft_text: str):

        edited = draft_text

        # Hidden editing policy

        if "UNKNOWN MEDICATION" in edited:

            edited = edited.replace(
                "UNKNOWN MEDICATION",
                "MEDICATION_REQUIRES_REVIEW"
            )

        if (
            "No reconciliation findings"
            in edited
        ):

            edited = edited.replace(
                "No reconciliation findings",
                "Medication reconciliation requires review"
            )

        return edited