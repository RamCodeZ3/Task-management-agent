import redis
from rq import Queue
from handlers.worker_logic import process_task
import os
from dotenv import load_dotenv


load_dotenv()

REDIS_TOKEN = os.getenv("REDIS_TOKEN")
connection = redis.Redis.from_url(REDIS_TOKEN)
task_queue = Queue("tasks", connection=connection)


async def enqueue_message(message_data: str, token_google: str):
    try:
        task_queue.enqueue(process_task, message_data, token_google)
    
    except Exception as e:
        raise ValueError("There was an error with redis:", e)
