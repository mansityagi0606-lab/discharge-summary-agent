import re

from app.tools.evidence_extractor import (
    EvidenceExtractor
)


class StructuredMedicationExtractor:

    def __init__(self):

        self.evidence_tool = (
            EvidenceExtractor()
        )

    def run(self, text: str):

        medications = []

        match = re.search(
            r"ADVICE ON DISCHARGE:(.*?)(FOLLOW-UP INSTRUCTIONS:)",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        if not match:
            return medications

        section = match.group(1)

        lines = section.split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if "TAB" not in line.upper():
                continue

            medication = {
                "name": None,
                "frequency": None,
                "duration": None,
                "evidence": line,
                "section": "ADVICE ON DISCHARGE"
            }

            freq_match = re.search(
                r"\d-\d-\d",
                line
            )

            if freq_match:
                medication["frequency"] = (
                    freq_match.group()
                )

            duration_match = re.search(
                r"(\d+)\s*DAYS",
                line,
                flags=re.IGNORECASE
            )

            if duration_match:
                medication["duration"] = (
                    duration_match.group()
                )

            name_match = re.search(
                r"TAB\.?\s*([A-Z0-9\s]+)",
                line,
                flags=re.IGNORECASE
            )

            if name_match:

                medication["name"] = (
                    name_match.group(1)
                    .strip()
                )

            medications.append(
                medication
            )

        return medications