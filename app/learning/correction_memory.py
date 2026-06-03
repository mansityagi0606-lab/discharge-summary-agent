import json
import os


class CorrectionMemory:

    FILE_PATH = "outputs/correction_memory.json"

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

        except (
            json.JSONDecodeError,
            OSError
        ):

            return []

    def save(
        self,
        correction
    ):

        memory = self.load()

        memory.append(
            correction
        )

        with open(
            self.FILE_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                memory,
                f,
                indent=4,
                ensure_ascii=False
            )

    def get_best_corrections(
        self,
        min_reward=0.9
    ):

        memory = self.load()

        return [
            item
            for item in memory
            if item.get(
                "reward",
                0
            ) >= min_reward
        ]

    def count(self):

        return len(
            self.load()
        )

    def clear(self):

        with open(
            self.FILE_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                [],
                f,
                indent=4
            )