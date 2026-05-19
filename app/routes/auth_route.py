from datetime import UTC
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from services.database_service.token import (
    TokenSecretServiceDB,
    TokenServiceDB,
)
from services.database_service.user import UserServiceDB
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.token import CreateToken, CreateTokenSecret
from schemas.user import CreateUser
from utils.db import get_db
from utils.jwt import create_jwt

route = APIRouter(prefix="/auth", tags=["Auth"])

SCOPES = [
    "https://www.googleapis.com/auth/tasks",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

PATH_ORIGIN = Path(__file__).parent.parent.parent
CREDENTIALS_PATH = PATH_ORIGIN / "credentials.json"
_flow_store = {}


@route.get("/login")
def login():
    flow = Flow.from_client_secrets_file(
        str(CREDENTIALS_PATH),
        scopes=SCOPES,
        redirect_uri="http://localhost:8000/auth/callback",
    )
    auth_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
    )
    _flow_store[state] = flow
    return RedirectResponse(auth_url)


@route.get("/callback")
async def callback(code: str, state: str, db: AsyncSession = Depends(get_db)):
    flow = _flow_store.pop(state, None)
    if not flow:
        return JSONResponse(
            {"error": "state inválido o expirado"}, status_code=400
        )

    flow.fetch_token(code=code)
    creds = flow.credentials

    service = build("oauth2", "v2", credentials=creds)
    user_info = service.userinfo().get().execute()

    user_db = UserServiceDB(db)
    token_db = TokenServiceDB(db)
    token_secret_db = TokenSecretServiceDB(db)

    user = CreateUser(display_name=user_info["name"], email=user_info["email"])
    user_result = await user_db.create_user(user)

    token = CreateToken(
        user_id=user_result.id,
        token_access=creds.token,
        token_uri=creds.token_uri,
        client_id=creds.client_id,
        scopes=" ".join(creds.scopes),
        expiry=creds.expiry.replace(tzinfo=UTC).isoformat(),
    )
    token_secret = CreateTokenSecret(
        user_id=user_result.id, refresh_token=creds.refresh_token
    )

    await token_db.create_token(token)
    await token_secret_db.create_token_secret(token_secret)

    jwt_token = create_jwt(str(user_result.id))

    return {
        "email": user_result.email,
        "access_token": jwt_token,
        "token_type": "Bearer",
    }
