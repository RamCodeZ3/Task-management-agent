import requests
import json
import os


ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_ID")


class WhatsappService:
    async def send_message(self, phone_number: str, message: str):
        try:
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }

            response = requests.post(
                f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages",
                headers=headers,
                json=payload
            )
            print(response.status_code)
            print(response.json())
        
        except Exception as e:
            raise ValueError("There was an error sending: ", e)


whatsapp_service = WhatsappService()
