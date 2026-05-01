from models.task import TaskModel
from services.extract_date.extract_date import DateExtractorService
from services.google_services.google_task import GoogleTask
from services.google_services.google_task_list import GoogleTaskList
from services.llm_services.llm_service import LLMService


async def process_task(message: str):
    llm = LLMService()
    gt = GoogleTask()
    gtl = GoogleTaskList()
    dtx = DateExtractorService()

    task_info = await llm.process(message)
    task_list_id = await gtl.get_task_list_by_title(
        task_info["classification"]["top_label"]
    )

    if not task_list_id:
        task_list_id = await gtl.create_task_list(
            f"{task_info['classification']['top_label']}"
        )

    deadline = dtx.extract_date(message)

    task = TaskModel(
        title=task_info["title"],
        notes=task_info["description"],
        deadline=str(deadline),
    )

    await gt.create_task(task, task_list_id)
    print("Se creo la tarea correctamente.")
