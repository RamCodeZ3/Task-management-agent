from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleTaskList:
    def __init__(self, credentials):
        self.service = build("tasks", "v1", credentials=credentials)

    async def create_task_list(self, title: str):
        try:
            body = {"title": title}
            task_list = self.service.tasklists().insert(body=body).execute()
            return task_list["id"]

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

    async def get_task_list_by_title(self, task_list_title: str):
        try:
            task_list = self.service.tasklists().list().execute()

            for tl in task_list["items"]:
                if tl["title"] == task_list_title:
                    return tl["id"]

            return None

        except HttpError as e:
            raise ValueError(f"There was an http error: {e}")

        except Exception as e:
            raise ValueError(f"There was an error getting the task list: {e}")
