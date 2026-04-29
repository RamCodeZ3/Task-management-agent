from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .auth_google import get_credentials


class GoogleTaskList:
    def __init__(self):
        self.service = build(
            "tasks",
            "v1",
            credentials=get_credentials()
        )
    
    async def create_task_list(self, title: str):
        try:
            body = {"title": title}
            task_list = self.service.tasklists().insert(body=body).execute()
            return task_list
        
        except HttpError as e:
            raise ValueError("There was an http error: ", e)
        
        except Exception as e:
            raise ValueError("There was an error creating the task list: ", e)
    
    async def get_all_task_lists(self):
        try:
            task_lists = self.service.tasklists().list().execute()
            return task_lists["items"]
        
        except HttpError as e:
            raise ValueError("There was an http error: ", e)
        
        except Exception as e:
            raise ValueError("There was an error getting the task lists: ", e)
    
    async def get_task_list_by_id(self, task_list_id: str):
        try:
            task_list = self.service.tasklists.get(
                tasklist=task_list_id
            ).execute()

            return task_list
        
        except HttpError as e:
            raise ValueError("There was an http error: ", e)

        except Exception as e:
            raise ValueError("There was an error getting the task list:", e)
