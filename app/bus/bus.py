import os

import redis
from dotenv import load_dotenv
from rq import Queue

from handlers.worker_logic import process_task

load_dotenv()

REDIS_TOKEN = os.getenv("REDIS_TOKEN")
connection = redis.Redis.from_url(REDIS_TOKEN)
task_queue = Queue("tasks", connection=connection)


async def enqueue_message(message_data: str, user_id: str):
    try:
        task_queue.enqueue(process_task, message_data, user_id)

    except Exception as e:
        raise ValueError("There was an error with redis:", e)
