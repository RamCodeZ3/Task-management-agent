from services.llm_services.classification_llm import classify
from services.llm_services.generation_llm import (
    generate_description,
    generate_title,
)


LABELS_CLASSIFY = [
    "personal tasks",
    "shopping",
    "work tasks",
    "important",
    "household chores",
]


class LLMService:
    async def process(self, text: str):
        return {
            "title": generate_title(text),
            "description": generate_description(text),
            "classification": classify(text, LABELS_CLASSIFY),
        }

llm_service = LLMService()
