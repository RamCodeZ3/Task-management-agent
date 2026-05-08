from google_auth_oauthlib.flow import Flow
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from pathlib import Path


route = APIRouter(prefix="/auth", tags=["Auth"])
SCOPES = ["https://www.googleapis.com/auth/tasks"]
PATH_ORIGIN = Path(__file__).parent.parent.parent
CREDENTIALS_PATH = PATH_ORIGIN / "credentials.json"

_flow_store = {}


@route.get("/login")
def login():
    flow = Flow.from_client_secrets_file(
        str(CREDENTIALS_PATH),
        scopes=SCOPES,
        redirect_uri="http://localhost:8000/auth/callback"
    )
    auth_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
    )
    _flow_store[state] = flow
    return RedirectResponse(auth_url)


@route.get("/callback")
def callback(code: str, state: str):
    flow = _flow_store.pop(state, None)
    if not flow:
        return JSONResponse(
            {"error": "state inválido o expirado"},
            status_code=400
        )

    flow.fetch_token(code=code)
    creds = flow.credentials

    return {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
    }
