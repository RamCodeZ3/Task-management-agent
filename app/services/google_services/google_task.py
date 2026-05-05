from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.models import task
from .auth_google import get_credentials
from models.task import TaskModel
from .google_task_list import google_task_list

class GoogleTask:
    def __init__(self):
        self.service = build(
            "tasks",
            "v1",
            credentials=get_credentials()
        )
    
    async def create_task(self, task: TaskModel, task_list_id: str):
        try:
            body = {
                "title": task.title,
                "notes": task.notes,
                "due": task.deadline
            }
            task = self.service.tasks().insert(
                tasklist=task_list_id,
                body=body
            ).execute()
            
            return task
        
        except HttpError as e:
            raise ValueError("There was an http error: ", e)
        
        except Exception as e:
            raise ValueError("There was an error creating the task: ", e)
    
    async def get_all_tasks(self, task_list_id: str):
        try:
            tasks = self.service.tasks().list(
                tasklist=task_list_id
            ).execute()
            return tasks["items"]
        
        except HttpError as e:
            raise ValueError("There was an http error: ", e)
        
        except Exception as e:
            raise ValueError("There was an error getting the tasks: ", e)

    async def get_tasks_by_date(self, date: str):
        try:
            tasks_lists = await google_task_list.get_all_task_lists()
            tasks_by_date = []

            for task_list in tasks_lists:
                tasks = await self.get_all_tasks(task_list["id"])

                for t in tasks:
                    if t["due"] == date:
                        tasks_by_date.append({
                            "title": t["title"],
                            "notes": t["notes"]
                        })
            return tasks_by_date
            
        except HttpError as e:
            raise ValueError("There was an http error: ", e)
        
        except Exception as e:
            raise ValueError("There was an error getting the tasks: ", e)


        
    async def update_task(
            self,
            task: TaskModel,
            task_list_id: str,
            task_id: str
        ):
        try:
            body = {
                "title": task.title,
                "notes": task.notes,
                "due": task.deadline
            }
            task = self.service.tasks().patch(
                tasklist=task_list_id,
                task=task_id,
                body=body
            ).execute()
            
            return task
        
        except HttpError as e:
            raise ValueError("There was an http error: ", e)
        
        except Exception as e:
            raise ValueError("There was an error updateting the task: ", e)
    

    async def delete_task(self, task_list_id: str, task_id: str):
        try:
            task = self.service.tasks().delete(
                tasklist=task_list_id,
                task=task_id
            ).execute()
        
        except HttpError as e:
            raise ValueError("There was an http error: ", e)
        
        except Exception as e:
            raise ValueError("There was an error deleting the task: ", e)

google_task = GoogleTask()
