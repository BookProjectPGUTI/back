from typing import Dict, Any
from uuid import UUID

from sqlalchemy import text, select, func

from src.domain.abc.dal import ABCDAL
from src.domain.user.model import User


class UserDAL(ABCDAL):
    model = User

    async def insert(self, data: Dict[str, Any]) -> UUID:
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
