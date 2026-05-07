from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.oauth2.credentials import Credentials
from pathlib import Path
import json


security = HTTPBearer()
PATH_ORIGIN = Path(__file__).parent.parent.parent.parent
CREDENTIALS_PATH = PATH_ORIGIN / "credentials.json"


def get_google_creds(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Credentials:
    try:
        with open(CREDENTIALS_PATH) as f:
            data = json.load(f)

        client_info = data.get("web") or data.get("installed")

        if not client_info:
            raise ValueError(
                f"Formato de credentials.json no reconocido. "
                f"Claves encontradas: {list(data.keys())}"
            )

        return Credentials(
            token=credentials.credentials,
            client_id=client_info["client_id"],
            client_secret=client_info["client_secret"],
            token_uri=client_info.get("token_uri", "https://oauth2.googleapis.com/token"),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}"
        )

def get_raw_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    return credentials.credentials

