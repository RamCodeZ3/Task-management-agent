from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from schemas.token import (
    CreateToken,
    TokenModel,
    CreateTokenSecret,
    TokenSecretModel
)
from models.user_token import Token
from models.token_secret import TokenSecret
from utils.encryption import encrypt, decrypt


class TokenServiceDB:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_token(self, data: CreateToken) -> TokenModel:
        try:
            db_token = Token(**data.model_dump())
            self.db.add(db_token)
            await self.db.commit()
            await self.db.refresh(db_token)
            return TokenModel.model_validate(db_token)
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(f"Violation of integrity: {e}")
        except Exception as e:
            raise ValueError(f"There was an unexpected error: {e}")

    async def get_token_by_user_id(self, user_id: str) -> TokenModel | None:
        try:
            result = await self.db.execute(
                select(Token).where(Token.user_id == user_id)
            )
            token = result.scalar_one_or_none()
            return TokenModel.model_validate(token) if token else None
        except Exception as e:
            raise ValueError(f"There was an unexpected error: {e}")


class TokenSecretServiceDB:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_token_secret(
        self,
        data: CreateTokenSecret
        ) -> TokenSecretModel:
        try:
            token_secret = TokenSecret(
                user_id=data.user_id,
                refresh_token=encrypt(data.refresh_token)
            )
            self.db.add(token_secret)
            await self.db.commit()
            await self.db.refresh(token_secret)
            return TokenSecretModel.model_validate(token_secret)
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(f"Violation of integrity: {e}")
        except Exception as e:
            raise ValueError(f"There was an unexpected error: {e}")

    async def get_refresh_token_by_user_id(self, user_id: str) -> str | None:
        try:
            result = await self.db.execute(
                select(TokenSecret).where(TokenSecret.user_id == user_id)
            )
            secret = result.scalar_one_or_none()
            return decrypt(secret.refresh_token) if secret else None
        
        except Exception as e:
            raise ValueError(f"There was an unexpected error: {e}")
