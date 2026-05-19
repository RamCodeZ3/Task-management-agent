from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form
)
from typing import Optional
from services.google_services.google_task import GoogleTask
from utils.transcriber import transcribe_audio_to_text
from bus.bus import enqueue_message
from .dependencies.auth import get_current_user
from utils.credential import build_credentials_from_db
from utils.db import AsyncSessionLocal


route = APIRouter(
    prefix="/task",
    tags=["Task"]
)


@route.post("/generate-task", status_code=status.HTTP_201_CREATED)
async def generate_task(
    message: Optional[str] = Form(default=None),
    audio: Optional[UploadFile] = File(default=None),
    current_user: str = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User token required"
        )

    if audio:
        audio_bytes = await audio.read()
        message = await transcribe_audio_to_text(
            audio_bytes,
            str(audio.filename)
        )
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="message or audio required"
        )

    await enqueue_message(message, current_user)
    return {"status": "The task is in the queue."}


@route.get("/", status_code=status.HTTP_200_OK)
async def get_task(
    task_list_id: str,
    current_user: str = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User token required"
        )
    if not task_list_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="task list id required"
        )
    
    async with AsyncSessionLocal() as db:
        creds = await build_credentials_from_db(current_user, db)

    google_task = GoogleTask(creds)
    task = await google_task.get_all_tasks(task_list_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tasks not found"
        )
    return {"items": task}


@route.get("/pending_task", status_code=status.HTTP_200_OK)
async def get_pending_tasks(
    current_user: str = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User token required"
        )
    async with AsyncSessionLocal() as db:
        creds = await build_credentials_from_db(current_user, db)
    
    google_task = GoogleTask(creds)
    pending_tasks = await google_task.get_pending_tasks()

    if not pending_tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="items not found"
        )

    return {"items": pending_tasks}


@route.get("/{date}", status_code=status.HTTP_200_OK)
async def get_task_by_date(
    date: str,
    current_user: str = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User token required"
        )
    async with AsyncSessionLocal() as db:
        creds = await build_credentials_from_db(current_user, db)

    google_task = GoogleTask(creds)
    tasks = await google_task.get_tasks_by_date(date)

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="items not found"
        )
    return {"items": tasks}

