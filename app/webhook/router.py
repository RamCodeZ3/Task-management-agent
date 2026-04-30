import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query, Request
from services.llm_services.llm_service import llm_service

from .parser import parser_message

load_dotenv()
webhook_token = os.getenv("WEBHOOK_TOKEN")

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.get("/")
async def verification(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    try:
        if hub_mode == "subscribe" and hub_verify_token == webhook_token:
            print("✅ Verified correctly")
            return int(hub_challenge)

        if not hub_mode or not hub_verify_token or not hub_challenge:
            raise HTTPException(status_code=400, detail="parameters are missing")

    except HTTPException:
        raise HTTPException(status_code=403, detail="Forbidden")

    except Exception as e:
        raise ValueError("There was a error with verification:", e)


@router.post("/")
async def message_entry(request: Request):
    try:
        data = await request.json()

        if data:
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    phone_number_id = value.get("metadata", {}).get("phone_number_id")
                    message_data = value.get("messages", [])
                    for message in message_data:
                        print(parser_message(message))

        return {"status": "EVENT_RECEIVED"}

    except Exception as e:
        raise ValueError("There was a error with message entry:", e)


@router.post("/LLM/generation")
async def generation(text: str):
    try:
        result = await llm_service.process(text)
        return result

    except Exception as e:
        raise Exception("There was a error with LLM process", e)
