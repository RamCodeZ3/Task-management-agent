from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import CreateUser, UserModel


class UserServiceDB:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, user: CreateUser) -> UserModel:
        try:
            db_user = User(**user.model_dump())
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            return UserModel.model_validate(db_user)

        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(f"Violation of integrity: {e}")
        except Exception as e:
            raise ValueError(f"There was an unexpected error: {e}")

    async def get_user_by_email(self, email: str) -> UserModel | None:
        try:
            result = await self.db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            return UserModel.model_validate(user) if user else None

        except Exception as e:
            raise ValueError(f"There was an unexpected error: {e}")
