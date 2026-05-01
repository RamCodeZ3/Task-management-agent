from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .auth_google import get_credentials
from models.task import TaskModel


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
