import os

from dotenv import load_dotenv
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


load_dotenv()

MODEL_NAME = os.getenv("GENERATION_LLM", "google/flan-t5-base")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def generate(prompt: str, max_new_tokens=50):
    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def generate_title(text: str) -> str:
    promt = f"Generate a concise title for the following text:\n{text}"
    return generate(promt, max_new_tokens=20)


def generate_description(text: str) -> str:
    prompt = f"Write a short description for the following content:\n{text}"
    return generate(prompt, max_new_tokens=60)
