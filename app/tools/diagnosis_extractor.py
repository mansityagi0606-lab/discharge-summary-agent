import re

from app.tools.evidence_extractor import (
    EvidenceExtractor
)


class DiagnosisExtractor:

    def __init__(self):

        self.evidence_tool = (
            EvidenceExtractor()
        )

    def run(self, text: str):

        diagnoses = []

        pattern = r"DIAGNOSIS:(.*?)HISTORY:"

        match = re.search(
            pattern,
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        if not match:
            return diagnoses

        section = match.group(1)

        for line in section.split("\n"):

            line = line.strip()

            if not line:
                continue

            if re.match(r"^\d+\)", line):

                diagnosis = re.sub(
                    r"^\d+\)\s*",
                    "",
                    line
                )

                diagnoses.append(
                    self.evidence_tool.create_evidence(
                        value=diagnosis,
                        source_text=line,
                        section="DIAGNOSIS"
                    )
                )

        return diagnoses