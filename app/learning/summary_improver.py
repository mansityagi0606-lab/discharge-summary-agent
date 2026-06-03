class SummaryImprover:

    def improve(
        self,
        summary_text,
        memory_entries
    ):

        improved = summary_text

        for entry in memory_entries:

            draft = entry.get(
                "draft",
                ""
            )

            edited = entry.get(
                "edited",
                ""
            )

            if (
                "UNKNOWN MEDICATION"
                in draft
                and
                "MEDICATION_REQUIRES_REVIEW"
                in edited
            ):

                improved = improved.replace(
                    "UNKNOWN MEDICATION",
                    "MEDICATION_REQUIRES_REVIEW"
                )

        return improved