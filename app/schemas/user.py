from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    display_name: str
    email: EmailStr


class UserModel(BaseModel):
    id: UUID
    display_name: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}
