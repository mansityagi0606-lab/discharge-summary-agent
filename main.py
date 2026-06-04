from app.agents.state import AgentState
from app.agents.discharge_agent import DischargeAgent
from app.learning.learning_manager import LearningManager


def run_patient(file_path: str):

    print("\n" + "=" * 60)
    print(f"RUNNING PATIENT: {file_path}")
    print("=" * 60)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # -------------------------
    # Agent Execution
    # -------------------------
    state = AgentState(raw_text=text)
    agent = DischargeAgent(state)
    result = agent.run()

    # -------------------------
    # Learning Loop (Part 2)
    # -------------------------
    learning = LearningManager()

    improved = learning.improve_draft(result.summary_draft)
    result.summary_draft = improved

    feedback = learning.learn_from_draft(improved)

    # -------------------------
    # Output Metrics
    # -------------------------
    print("\n=== LEARNING METRIC ===")
    print("Reward Score:", feedback["reward"])
    print("Average Reward:", learning.metrics.average_reward())

    # -------------------------
    # Key Outputs
    # -------------------------
    print("\nDIAGNOSES")
    print(result.diagnoses)

    print("\nSTRUCTURED MEDICATIONS")
    print(result.structured_medications)

    print("\nMISSING FIELDS")
    print(result.missing_fields)

    print("\nPENDING ITEMS")
    print(result.pending_items)

    print("\nCONFLICTS")
    print(result.conflicts)

    print("\nSAFETY FLAGS")
    print(result.safety_flags)

    print("\nSUMMARY DRAFT")
    print(result.summary_draft)

    return result


# =========================
# MAIN EXECUTION
# =========================
if __name__ == "__main__":

    files = [
        "ocr_output.txt",
        "ocr_output_2.txt"
    ]

    results = []

    for file in files:
        result = run_patient(file)
        results.append(result)

    print("\n" + "=" * 60)
    print("ALL PATIENTS COMPLETED")
    print("=" * 60)