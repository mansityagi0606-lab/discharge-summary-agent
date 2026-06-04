AI Discharge Summary Agent (LLM + Tool-Using Clinical Assistant)

An AI-powered agent that processes noisy OCR discharge summaries and generates structured, traceable, and clinically safe draft reports.
The system simulates a real-world clinical documentation assistant with tool-based reasoning, iterative planning, and a learning loop from reviewer feedback.

Key Features:
Agentic reasoning loop (plan → act → re-plan)
PDF/OCR ingestion pipeline
Structured extraction of diagnoses & medications
Medication reconciliation (admission vs discharge)
Conflict detection + safety flagging
Drug interaction checks (mock tool-based safety layer)
Hard no-fabrication guardrail (critical design constraint)
Trace logging for every decision step
Learning loop using simulated reviewer feedback (Part 2)
System Architecture

The system is built around a stateful agent loop:
OCR Text → Agent State → Planner → Tool Selection → State Update → Repeat → Summary Generation
Agent Loop Design
At each iteration:
Planner analyzes current AgentState
Chooses next action:
extract_diagnosis
extract_medications
reconcile_medications
generate_summary
finish
Tool executes and updates state
Trace is logged
Agent re-plans until completion or step limit

This ensures the system is not a fixed pipeline, but a dynamic reasoning loop.

No Fabrication Guardrail (Core Safety Feature):

The agent is strictly designed to never hallucinate clinical information.

Enforcement Strategy:
Only extracted values from OCR are used
Missing fields are explicitly marked:
"MISSING (Clinician Review Required)"
Pending labs are explicitly preserved
Conflicts are flagged instead of resolved
No “best guess” filling is allowed anywhere in pipeline
If data is not present in the document → it is never invented.

onflict & Safety Handling:
The system detects and escalates:
Duplicate or inconsistent diagnoses
Missing medication mapping
History vs discharge medication mismatch
Drug interaction risks (mock interaction tool)


Medication Reconciliation:
The system compares:
Admission medications
Discharge medications

It detects:
Added medications
Stopped medications
Unexplained changes

If no admission data exists, reconciliation is safely skipped.

Traceability (Observability Layer):
Every step is logged in a structured trace:

{
  "reasoning": "...",
  "tool": "DiagnosisExtractor",
  "input": "raw_text",
  "result": "...",
  "next_action": "re-plan"
}

This ensures:

Full auditability
Debugging support
Clinical transparency

Part 2: Learning from Reviewer Feedback
Since real clinician edits are unavailable, a simulated reviewer is used.

Approach
Agent generates draft summary
Simulated reviewer applies hidden edit policy
Produces (draft → edited) pair
System computes:
Reward Signal
Edit distance between draft and corrected version
Section-level similarity score
Learning Objective

The system improves by:
Reducing unnecessary edits
Increasing structural correctness
Maintaining clinical fidelity (NOT verbosity reduction)
Output Metrics
Example:
Reward Score: 0.98 → 1.0
Average Reward tracked over runs
Learning curve stored in learning_metrics.json


How to Run:
1. Install dependencies
   pip install -r requirements.txt
2. Run Agent
   python main.py
3. Outputs generated in:
   /outputs
  ├── trace.json
  ├── summary_final.txt
  ├── learning_metrics.json

Project Structure:
app/
 ├── agents/
 ├── tools/
 ├── utils/
 ├── learning/
main.py
ocr_output.txt
outputs/

Summary:
This project demonstrates a production-style AI agent system with:
Tool-based reasoning loop
Clinical safety constraints
Structured extraction pipeline
Traceable decision-making
Self-improving learning simulation
It is designed as a safe, auditable, and extensible clinical AI assistant prototype.
