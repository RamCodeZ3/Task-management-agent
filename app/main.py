from services.google_services.google_task_list import GoogleTaskList
from services.google_services.google_task import GoogleTask
from models.task import TaskModel
import asyncio

if __name__ == "__main__":
    gtl = GoogleTaskList()
    gt = GoogleTask()
    
    # task_list = asyncio.run(gtl.get_all_task_lists())

    task = TaskModel(
        title="Trabajo de fundamento de programacion",
        notes="Crea un programa que utilice programacion orientada a objeto",
        deadline="2026-05-10T10:30:00-04:00"
    )

    asyncio.run(gt.create_task(task, "WnhCQktLejRSNUV2N0pRTQ"))

    print(task)