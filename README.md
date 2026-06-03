AI Discharge Summary Agent (Clinical Document Intelligence System)

An autonomous AI agent that reads clinical discharge PDFs (via OCR text) and generates a structured, evidence-grounded discharge summary using a multi-step reasoning loop with tool-based extraction, safety checks, and a self-improving learning mechanism.

Key Highlights
Agentic workflow (planner + re-plan loop)
OCR-based medical document ingestion
Structured extraction (diagnosis + medications)
Medication reconciliation engine
Conflict + safety detection system
Evidence-grounded outputs (no hallucination policy)
Traceable execution logs (audit-ready)
Learning loop using correction feedback + reward scoring

System Architecture
OCR Text Input
      ↓
Agent Planner (decides next step)
      ↓
Tool Execution Layer
 ├── Diagnosis Extractor
 ├── Medication Extractor
 ├── Structured Medication Parser
 ├── Reconciliation Engine
 ├── Conflict Checker
 ├── Drug Interaction Checker
      ↓
State Manager (AgentState)
      ↓
Safety + Validation Layer
      ↓
Summary Generator
      ↓
Trace Logger + Learning System

How It Works
The system operates as a controlled reasoning agent loop:
Reads raw OCR discharge text
Planner decides next action dynamically
Executes tools (extraction / validation / reconciliation)
Updates shared agent state
Re-plans until completion or step limit reached
Generates final structured discharge summary
Logs every step for auditability

Core Features
1. PDF / OCR Ingestion
Processes raw OCR-extracted discharge summaries
Robust section parsing (Diagnosis, Medications, Follow-up, etc.)

2. Structured Medical Extraction
Extracts:
Diagnoses
Medications
Frequency & duration
Preserves evidence mapping for every extracted field

3. Medication Reconciliation
Compares:
Admission medications
Discharge medications

Detects:
Added medications
Stopped medications
Unexplained changes

4. Clinical Safety Layer
Automatically flags:
Conflicting diagnoses
Missing clinical information
Drug interactions (rule-based mock tool)
History–discharge mismatches

5. Agentic Planning Loop

Instead of a fixed pipeline, the system uses a planner:

Decides next action dynamically
Supports re-planning based on intermediate results
Prevents premature completion

6. Observability & Traceability

Every step is logged:

{
  "reasoning": "Need diagnosis extraction",
  "tool": "DiagnosisExtractor",
  "input": "raw_text",
  "result": "...",
  "next_action": "re-plan"
}

This ensures:

Full audit trail
Debuggable AI decisions
Clinical transparency

7. Learning System (Feedback Loop)

The system simulates clinician review:
Generates correction signals (simulated doctor edits)
Computes reward score based on edit distance
Stores correction memory
Improves future outputs using feedback

Goal: reduce human editing burden over time

Example Output
===== DISCHARGE SUMMARY DRAFT =====

Diagnoses:
- ACUTE GASTROENTERITIS WITH DEHYDRATION
- URINARY TRACT INFECTION

Discharge Medications:
- RACIPER 40MG (1-0-0, 7 DAYS)
- EMESET (3 DAYS)

Pending Results:
- Urine culture report awaited

Medication Reconciliation:
- REVIEW REQUIRED: Missing thyroid medication in discharge list

Conflicts:
- Multiple diagnosis sections detected

Safety Flags:
- None
