from services.llm_services.classification_llm import classify
from services.llm_services.generation_llm import generate_title, summarize


class LLMService:
    async def process(self, text: str):
        return {
            "title": generate_title(text),
            "summary": summarize(text),
            "classification": classify(text, ["tech", "business", "science"]),
        }


llm_service = LLMService()
