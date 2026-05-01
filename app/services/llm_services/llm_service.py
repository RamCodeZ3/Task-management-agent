from services.llm_services.classification_llm import classify
from services.llm_services.generation_llm import generate_description, generate_title


INTENT_LABELS_DESCRIPTIVE = [
    "create a new task",
    "update an existing task",
    "delete a task",
    "get or list tasks",
]

INTENT_LABELS = ["Create task", "Update task", "Delete task", "Get Task"]

LABELS_CLASSIFY = ["tech", "business", "science"]


class LLMService:
    async def process(self, text: str):
        return {
            "title": generate_title(text),
            "description": generate_description(text),
            "classification": classify(text, LABELS_CLASSIFY),
        }

    def classify_intent(self, text: str):
        classification = classify(text, INTENT_LABELS_DESCRIPTIVE)
        return INTENT_LABELS[
            INTENT_LABELS_DESCRIPTIVE.index(classification["top_label"])
        ]


llm_service = LLMService()
