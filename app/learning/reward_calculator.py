from difflib import SequenceMatcher


class RewardCalculator:

    def calculate(
        self,
        draft_text,
        edited_text
    ):

        similarity = (
            SequenceMatcher(
                None,
                draft_text,
                edited_text
            ).ratio()
        )

        return round(similarity, 4)