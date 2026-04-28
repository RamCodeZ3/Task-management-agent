from fastapi import APIRouter, Query, HTTPException, Request
from dotenv import load_dotenv
import os
from .parser import parser_message


load_dotenv()
webhook_token = os.getenv("WEBHOOK_TOKEN")

router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"]
)


@router.get("/")
async def verification(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == webhook_token:
        print("✅ verificado correctamente")
        return int(hub_challenge)
    
    if not hub_mode or not hub_verify_token or not hub_challenge:
        raise HTTPException(status_code=400, detail="parameters are missing")
    
    raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/")
async def message_entry(request: Request):
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
