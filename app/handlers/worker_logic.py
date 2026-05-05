from models.task import TaskModel
from services.extract_date.extract_date import date_extractor
from services.google_services.google_task import google_task
from services.google_services.google_task_list import google_task_list
from services.llm_services.llm_service import llm_service
from services.whatsapp_services.whatsapp_message import whatsapp_service


async def process_task(message: str, phone_number: str):
    try:
        action = llm_service.classify_intent(message)

        if action == "Create task":
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
            await whatsapp_service.send_message(
                f"✅ The task {task.title} was successfully created",
                phone_number
            )

        elif action == "Get task":
            date = date_extractor.extract_date(message)
            tasks = await google_task.get_tasks_by_date(str(date))
    
            if not tasks:
                await whatsapp_service.send_message(
                    f"📭 No tasks found for {date}.",
                    phone_number
                )
            else:
                lines = [f"📋 *Tasks for {date}:*\n"]
                for i, task in enumerate(tasks, start=1):
                    lines.append(f"{i}. *{task['title']}*")
                    if task.get("notes"):
                        lines.append(f"   📝 {task['notes']}")
        
                formatted_message = "\n".join(lines)
                await whatsapp_service.send_message(
                    formatted_message,
                    phone_number
                )
        
        else:
            await whatsapp_service.send_message(
                "I didn't understand your request.",
                phone_number
            )

    
    except Exception as e:
        raise ValueError("There was an error: ", e)

