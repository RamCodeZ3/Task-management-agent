import asyncio
from schemas.task import TaskModel
from services.extract_date.extract_date import date_extractor
from services.google_services.google_task import GoogleTask
from services.google_services.google_task_list import GoogleTaskList
from services.llm_services.llm_service import llm_service
from utils.credential import build_credentials_from_db
from utils.db import get_db


def process_task(message: str, user_id: str):
    asyncio.run(_process_task_async(message, user_id))


async def _process_task_async(message: str, user_id: str):
    try:
        token = build_credentials_from_db(user_id, get_db())
        creds = token
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

