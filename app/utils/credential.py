from pathlib import Path
from google.oauth2.credentials import Credentials
from sqlalchemy.ext.asyncio import AsyncSession
from services.database_service.token import TokenServiceDB
from services.database_service.token import TokenSecretServiceDB
from .encryption import decrypt
import json


PATH_ORIGIN = Path(__file__).parent.parent.parent
CREDENTIALS_PATH = PATH_ORIGIN / "credentials.json"

async def build_credentials_from_db(user_id: str, db: AsyncSession) -> Credentials:
    
    token_db = TokenServiceDB(db)
    token_secret_db = TokenSecretServiceDB(db)

    token = await token_db.get_token_by_user_id(user_id)
    if not token:
        raise ValueError(f"No user token found {user_id}")

    token_secret = await token_secret_db.get_refresh_token_by_user_id(user_id)
    if not token_secret:
        raise ValueError(f"No user secret token found {user_id}")

    with open(CREDENTIALS_PATH, "r") as f:
        credentials_data = json.load(f)
    
    client_config = credentials_data.get("web") or credentials_data.get("installed")
    client_secret = client_config.get("client_secret")
    

    return Credentials(
        token=token.token_access,
        refresh_token=decrypt(token_secret.refresh_token),
        token_uri=token.token_uri,
        client_id=token.client_id,
        client_secret=client_secret,
        scopes=token.scopes.split(" "),
    )
