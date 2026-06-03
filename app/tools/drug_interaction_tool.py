class DrugInteractionTool:

    INTERACTIONS = {
        ("warfarin", "aspirin"):
            "Increased bleeding risk",

        ("ibuprofen", "warfarin"):
            "Major bleeding risk"
    }

    def run(self, medication_names):

        findings = []

        meds = [
            m.lower()
            for m in medication_names
        ]

        for i in range(len(meds)):

            for j in range(i + 1, len(meds)):

                pair = (
                    meds[i],
                    meds[j]
                )

                reverse_pair = (
                    meds[j],
                    meds[i]
                )

                if pair in self.INTERACTIONS:

                    findings.append(
                        {
                            "pair": pair,
                            "risk":
                            self.INTERACTIONS[pair]
                        }
                    )

                elif reverse_pair in self.INTERACTIONS:

                    findings.append(
                        {
                            "pair": reverse_pair,
                            "risk":
                            self.INTERACTIONS[
                                reverse_pair
                            ]
                        }
                    )

        return findings