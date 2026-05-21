from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from schemas.task import TaskModel

from .google_task_list import GoogleTaskList


class GoogleTask:
    def __init__(self, credentials):
        self.credentials = credentials
        self.service = build("tasks", "v1", credentials=self.credentials)

    async def create_task(self, task: TaskModel, task_list_id: str):
        try:
            body = {
                "title": task.title,
                "notes": task.notes,
                "due": task.deadline,
            }
            task = (
                self.service.tasks()
                .insert(tasklist=task_list_id, body=body)
                .execute()
            )

            return task

        except HttpError as e:
            raise ValueError("There was an http error: ", e)

        except Exception as e:
            raise ValueError("There was an error creating the task: ", e)

    async def get_all_tasks(self, task_list_id: str):
        try:
            tasks = self.service.tasks().list(tasklist=task_list_id).execute()
            return tasks["items"]

        except HttpError as e:
            raise ValueError("There was an http error: ", e)

        except Exception as e:
            raise ValueError("There was an error getting the tasks: ", e)

    async def get_tasks_by_date(self, date: str):
        try:
            google_task_list = GoogleTaskList(self.credentials)
            tasks_lists = await google_task_list.get_all_task_lists()
            tasks_by_date = []

            for task_list in tasks_lists:
                tasks = await self.get_all_tasks(task_list["id"])

                for t in tasks:
                    task_due = t.get("due")
                    if not task_due:
                        continue

                    task_date = datetime.fromisoformat(
                        task_due.replace("Z", "+00:00")
                    ).strftime("%Y-%m-%d")

                    if task_date == date:
                        tasks_by_date.append(
                            {"title": t.get("title"), "notes": t.get("notes")}
                        )

            return tasks_by_date

        except HttpError as e:
            raise ValueError("There was an http error: ", e)

        except Exception as e:
            raise ValueError("There was an error getting the tasks: ", e)

    async def get_pending_tasks(self):
        try:
            google_task_list = GoogleTaskList(self.credentials)
            tasks_lists = await google_task_list.get_all_task_lists()
            pending_tasks = []
            for task_list in tasks_lists:
                tasks = (
                    self.service.tasks()
                    .list(tasklist=task_list["id"], showCompleted=False)
                    .execute()
                )

                for t in tasks.get("items", []):
                    pending_tasks.append(t)

            return pending_tasks

        except HttpError as e:
            raise ValueError("There was an http error: ", e)

        except Exception as e:
            raise ValueError("There was an error getting the tasks: ", e)

    async def update_task(
        self, task: TaskModel, task_list_id: str, task_id: str
    ):
        try:
            body = {
                "title": task.title,
                "notes": task.notes,
                "due": task.deadline,
            }
            task = (
                self.service.tasks()
                .patch(tasklist=task_list_id, task=task_id, body=body)
                .execute()
            )

            return task

        except HttpError as e:
            raise ValueError("There was an http error: ", e)

        except Exception as e:
            raise ValueError("There was an error updateting the task: ", e)

    async def delete_task(self, task_list_id: str, task_id: str):
        try:
            task = (
                self.service.tasks()
                .delete(tasklist=task_list_id, task=task_id)
                .execute()
            )
            return task

        except HttpError as e:
            raise ValueError("There was an http error: ", e)

        except Exception as e:
            raise ValueError("There was an error deleting the task: ", e)
