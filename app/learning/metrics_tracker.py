import json
import os


class MetricsTracker:

    FILE_PATH = (
        "outputs/learning_metrics.json"
    )

    def __init__(self):

        os.makedirs(
            "outputs",
            exist_ok=True
        )

    def load(self):

        if not os.path.exists(
            self.FILE_PATH
        ):
            return []

        try:

            with open(
                self.FILE_PATH,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return []

    def save_reward(
        self,
        reward
    ):

        metrics = self.load()

        metrics.append(
            {
                "iteration":
                len(metrics) + 1,

                "reward":
                reward
            }
        )

        with open(
            self.FILE_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                metrics,
                f,
                indent=4
            )

    def average_reward(self):

        metrics = self.load()

        if not metrics:
            return 0

        total = sum(
            item["reward"]
            for item in metrics
        )

        return round(
            total / len(metrics),
            4
        )