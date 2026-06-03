class EvidenceExtractor:

    def create_evidence(
        self,
        value: str,
        source_text: str,
        section: str
    ):

        return {
            "value": value,
            "evidence": source_text,
            "section": section
        }