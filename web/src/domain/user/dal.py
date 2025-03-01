from typing import Dict, Any
from uuid import UUID

from sqlalchemy import text, select, func, update

from src.domain.abc.dal import ABCDAL
from src.domain.user.model import User


class UserDAL(ABCDAL[User]):
    async def insert(self, data: Dict[str, Any]) -> UUID:  # noqa
        stmt = text(
            f"""
INSERT INTO "{self.model.__tablename__}" (
    {self.model.email.key}, 
    {self.model.username.key}, 
    {self.model.password.key}
)
VALUES (
    :{self.model.email.key}, 
    :{self.model.username.key}, 
    crypt(:{self.model.password.key}, gen_salt('bf'))
)
RETURNING {self.model.id.key};
            """
        )

        result = (await self.session.execute(stmt, data)).one()
        return result.id

    async def check_credentials(self, username: str, password: str) -> bool:
        stmt = select(
            self.model.id
        ).where(
            self.model.username == username,
            self.model.password == func.crypt(password, self.model.password)
        ).limit(1)

        result = (await self.session.execute(stmt)).one_or_none()
        return result is not None

    async def check_email_exists(self, email: str) -> bool:
        stmt = select(
            self.model.id
        ).where(
            self.model.email == email,
        ).limit(1)

        result = (await self.session.execute(stmt)).one_or_none()
        return result is not None

    async def check_username_exists(self, username: str) -> bool:
        stmt = select(
            self.model.id
        ).where(
            self.model.username == username,
        ).limit(1)

        result = (await self.session.execute(stmt)).one_or_none()
        return result is not None

    async def check_user_confirmed(self, user_id: UUID) -> bool:
        stmt = select(
            self.model.id
        ).where(
            self.model.id == user_id,
            self.model.is_confirmed.is_(True)
        ).limit(1)

        result = (await self.session.execute(stmt)).one_or_none()
        return result is not None

    async def check_user_enabled(self, user_id: UUID) -> bool:
        stmt = select(
            self.model.id
        ).where(
            self.model.id == user_id,
            self.model.is_enabled.is_(True)
        ).limit(1)

        result = (await self.session.execute(stmt)).one_or_none()
        return result is not None

    async def confirm_user(self, user_id: UUID):
        stmt = update(
            self.model
        ).values(
            **{
                self.model.is_confirmed.key: True
            }
        ).where(
            self.model.id == user_id
        )

        await self.session.execute(stmt)
