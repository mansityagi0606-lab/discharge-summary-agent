from app.agents.state import AgentState
from app.agents.discharge_agent import DischargeAgent
from app.learning.learning_manager import (LearningManager)

with open(
    "ocr_output.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()

state = AgentState(raw_text=text)

agent = DischargeAgent(state)

result = agent.run()

learning = (
    LearningManager()
)
result.summary_draft = (
    learning.improve_draft(
        result.summary_draft
    )
)

feedback = (
    learning.learn_from_draft(
        result.summary_draft
    )
)

print("\n=== LEARNING METRIC ===")
print(
    "Reward Score:",
    feedback["reward"]
)
print(
    "Average Reward:",
    learning.metrics.average_reward()
)

print("DIAGNOSES")
print(result.diagnoses)

print("\nDIAGNOSIS EVIDENCE")
print(result.diagnosis_evidence)

print("\nSTRUCTURED MEDICATIONS")
print(result.structured_medications)

print("\nSUMMARY DRAFT")
print(repr(result.summary_draft))