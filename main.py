from app.agents.state import AgentState
from app.agents.discharge_agent import DischargeAgent
from app.learning.learning_manager import LearningManager

import os


# -----------------------------
# Load OCR input
# -----------------------------
with open(
    "ocr_output.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()


# -----------------------------
# Initialize state + agent
# -----------------------------
state = AgentState(raw_text=text)

agent = DischargeAgent(state)

result = agent.run()


# -----------------------------
# Save raw agent outputs (IMPORTANT FOR SUBMISSION)
# -----------------------------
os.makedirs("outputs", exist_ok=True)

with open("outputs/summary_raw.txt", "w", encoding="utf-8") as f:
    f.write(result.summary_draft)


# -----------------------------
# Learning Layer
# -----------------------------
learning = LearningManager()

# Improve draft (post-processing / correction simulation)
improved_draft = learning.improve_draft(result.summary_draft)

result.summary_draft = improved_draft

# Learn from final draft
feedback = learning.learn_from_draft(result.summary_draft)


# -----------------------------
# Save learning outputs
# -----------------------------
with open("outputs/summary_final.txt", "w", encoding="utf-8") as f:
    f.write(result.summary_draft)

with open("outputs/learning_feedback.json", "w", encoding="utf-8") as f:
    import json
    json.dump(feedback, f, indent=2)


# -----------------------------
# Console output (evaluation view)
# -----------------------------
print("\n=== LEARNING METRIC ===")
print("Reward Score:", feedback["reward"])
print("Average Reward:", learning.metrics.average_reward())

print("\nDIAGNOSES")
print(result.diagnoses)

print("\nDIAGNOSIS EVIDENCE")
print(result.diagnosis_evidence)

print("\nSTRUCTURED MEDICATIONS")
print(result.structured_medications)

print("\nSUMMARY DRAFT")
print(result.summary_draft)