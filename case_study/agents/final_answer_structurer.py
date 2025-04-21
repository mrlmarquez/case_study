from smolagents import FinalAnswerTool

from case_study.models import LegalEntities


class FinalAnswerStructurer(FinalAnswerTool):
    name = "final_answer"
    description = (
        "Provides a final answer in `LegalEntities` format to the given problem."
    )
    inputs = {
        "answer": {
            "type": "str",
            "description": "The final answer (in JSON string format) to the problem",
        }
    }
    output_type = "LegalEntities"

    def forward(self, answer) -> LegalEntities:
        return LegalEntities.model_validate_json(answer)
