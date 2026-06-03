import re


class MedicationExtractor:

    def run(self, text: str):

        medications = []

        start_match = re.search(
            r"ADVICE ON DISCHARGE:(.*?)(FOLLOW-UP INSTRUCTIONS:)",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        if not start_match:
            return medications

        med_section = start_match.group(1)

        lines = med_section.split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if "TAB" in line.upper():

                medication = {
                    "raw_text": line
                }

                medications.append(medication)

        return medications