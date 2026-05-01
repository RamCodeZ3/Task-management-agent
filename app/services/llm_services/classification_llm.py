import os
from dotenv import load_dotenv
from transformers import pipeline


load_dotenv()

MODEL_NAME = os.getenv("CLASSIFICATION_LLM")

classifier_pipeline = pipeline("zero-shot-classification", model=MODEL_NAME)


def classify(text: str, labels: list[str]):
    result = classifier_pipeline(text, candidate_labels=labels)

    return {
        "labels": result["labels"],
        "scores": result["scores"],
        "top_label": result["labels"][0],
        "confidence": result["scores"][0],
    }
