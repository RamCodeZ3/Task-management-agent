from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CreateToken(BaseModel):
    user_id: UUID
    token_access: str
    token_uri: str
    client_id: str
    scopes: str
    expiry: str


class TokenModel(BaseModel):
    id: UUID
    user_id: UUID
    token_access: str
    token_uri: str
    client_id: str
    scopes: str
    expiry: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CreateTokenSecret(BaseModel):
    user_id: UUID
    refresh_token: str


class TokenSecretModel(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
