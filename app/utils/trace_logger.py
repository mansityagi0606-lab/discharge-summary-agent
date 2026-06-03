import json
from datetime import datetime


class TraceLogger:

    def __init__(self):
        self.logs = []

    def add(
        self,
        reasoning: str,
        tool: str,
        tool_input: str,
        result: str,
        next_action: str
    ):
        self.logs.append(
            {
                "timestamp": str(datetime.now()),
                "reasoning": reasoning,
                "tool": tool,
                "input": tool_input,
                "result": result,
                "next_action": next_action,
            }
        )

    def export(self, filepath="outputs/trace.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, indent=4)