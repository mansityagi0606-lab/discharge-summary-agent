from app.schemas.discharge_summary import MedicationData
from app.tools.llm import llm

structured_llm = llm.with_structured_output(MedicationData)


def extract_medications(document_text: str) -> MedicationData:

    prompt = f"""
You are a clinical medication extraction system.

Extract:

1. Admission Medications
2. Discharge Medications

RULES:

- Never guess.
- Never infer.
- Return empty lists if not found.

DOCUMENT:

{document_text}
"""

    return structured_llm.invoke(prompt)