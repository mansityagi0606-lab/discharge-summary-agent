from app.schemas.discharge_summary import Diagnosis
from app.tools.llm import llm

structured_llm = llm.with_structured_output(Diagnosis)


def extract_diagnosis(document_text: str) -> Diagnosis:

    prompt = f"""
You are an expert clinical information extraction system.

TASK:
Extract:

1. Principal Diagnosis
2. Secondary Diagnoses

RULES:

- NEVER invent information.
- Use ONLY explicitly documented diagnoses.
- If diagnosis is missing return null.
- Return structured data only.

DOCUMENT:

{document_text}
"""

    return structured_llm.invoke(prompt)