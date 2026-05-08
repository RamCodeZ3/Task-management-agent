from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.oauth2.credentials import Credentials
from pathlib import Path
import json


security = HTTPBearer()
PATH_ORIGIN = Path(__file__).parent.parent.parent.parent
CREDENTIALS_PATH = PATH_ORIGIN / "credentials.json"

class GoogleAuth:

    def get_google_creds(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> Credentials:
        try:
            token_data = json.loads(credentials.credentials)
        
            return Credentials(
                token=token_data["token"],
                refresh_token=token_data["refresh_token"],
                token_uri=token_data["token_uri"],
                client_id=token_data["client_id"],
                client_secret=token_data["client_secret"],
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token inválido: {str(e)}"
            )


    def get_raw_token(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> str:
        return credentials.credentials


google_auth = GoogleAuth()

