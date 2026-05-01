import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query, Request
from bus.bus import process_task, connection
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
            raise HTTPException(
                status_code=400,
                detail="parameters are missing"
            )

    except HTTPException:
        raise HTTPException(status_code=403, detail="Forbidden")

    except Exception as e:
        raise ValueError("There was a error with verification:", e)


async def _handle_message(request: Request):
    try:
        data = await request.json()
        if data:
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    message_data = value.get("messages", [])

                    for message in message_data:
                        message_id = message.get("id")

                        if not message_id:
                            continue

                        if connection.exists(f"msg:{message_id}"):
                            continue

                        connection.setex(
                            f"msg:{message_id}",
                            86400,
                            "processed"
                        )

                        extracted_message = parser_message(message)
                        await process_task(extracted_message)

        return {"status": "EVENT_RECEIVED"}
    except Exception as e:
        raise ValueError("There was an error:", e)


@router.post("/")
async def message_entry(request: Request):
    return await _handle_message(request)


@router.post("")
async def message_entry_no_slash(request: Request):
    return await _handle_message(request)
