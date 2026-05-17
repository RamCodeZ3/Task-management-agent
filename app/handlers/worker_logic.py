import asyncio
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from schemas.task import TaskModel
from services.extract_date.extract_date import date_extractor
from services.google_services.google_task import GoogleTask
from services.google_services.google_task_list import GoogleTaskList
from services.llm_services.llm_service import llm_service


def process_task(message: str, token: str):
    asyncio.run(_process_task_async(message, token))


async def _process_task_async(message: str, token: str):
    try:
        creds = _build_credentials(token)
        google_task = GoogleTask(creds)
        google_task_list = GoogleTaskList(creds)

        task_info = await llm_service.process(message)
        task_list_id = await google_task_list.get_task_list_by_title(
            task_info["classification"]["top_label"]
        )
        if not task_list_id:
            task_list_id = await google_task_list.create_task_list(
                f"{task_info['classification']['top_label']}"
            )
        deadline = date_extractor.extract_date(message)
        task = TaskModel(
            title=task_info["title"],
            notes=task_info["description"],
            deadline=str(deadline),
        )
        await google_task.create_task(task, task_list_id)

    except Exception as e:
        raise ValueError("There was an error: ", e)


PATH_ORIGIN = Path(__file__).parent.parent.parent
CREDENTIALS_PATH = PATH_ORIGIN / "credentials.json"


def _build_credentials(token: str) -> Credentials:
    token_data = json.loads(token)
    
    return Credentials(
        token=token_data["token"],
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get(
            "token_uri",
            "https://oauth2.googleapis.com/token"
        ),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
    )
