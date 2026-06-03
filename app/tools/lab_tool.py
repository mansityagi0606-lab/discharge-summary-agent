from app.schemas.discharge_summary import PendingResults
from app.tools.llm import llm

structured_llm = llm.with_structured_output(PendingResults)


def extract_pending_results(document_text: str) -> PendingResults:

    prompt = f"""
You are a clinical information extraction system.

Find:

- Pending investigations
- Awaited reports
- Pending cultures
- Pending laboratory tests

RULES:

- Only include explicitly pending items.
- Never invent information.

DOCUMENT:

{document_text}
"""

    return structured_llm.invoke(prompt)