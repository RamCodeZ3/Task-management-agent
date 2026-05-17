from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class CreateUser(BaseModel):
    display_name: str
    email: EmailStr


class UserModel(BaseModel):
    id: UUID
    display_name: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}

