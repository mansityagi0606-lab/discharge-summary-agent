from app.learning.doctor_reviewer import (
    DoctorReviewer
)

from app.learning.reward_calculator import (
    RewardCalculator
)

from app.learning.correction_memory import (
    CorrectionMemory
)

from app.learning.summary_improver import (
    SummaryImprover
)

from app.learning.metrics_tracker import (
    MetricsTracker
)


class LearningManager:

    def __init__(self):

        self.reviewer = (
            DoctorReviewer()
        )

        self.reward_tool = (
            RewardCalculator()
        )

        self.memory = (
            CorrectionMemory()
        )

        self.improver = (
            SummaryImprover()
        )
        self.metrics = (
            MetricsTracker()
        )

    def improve_draft(
        self,
        draft_text
    ):

        memory = (
            self.memory.load()
        )

        return self.improver.improve(
            draft_text,
            memory
        )

    def learn_from_draft(
        self,
        draft_text
    ):

        edited_text = (
            self.reviewer.review(
                draft_text
            )
        )

        reward = (
            self.reward_tool.calculate(
                draft_text,
                edited_text
            )
        )

        self.memory.save(
            {
                "draft":
                draft_text,

                "edited":
                edited_text,

                "reward":
                reward
            }
        )
        
        self.metrics.save_reward(
            reward
        )

        return {
            "edited_text":
            edited_text,

            "reward":
            reward
        }