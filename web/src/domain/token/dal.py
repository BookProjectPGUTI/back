from uuid import UUID

from sqlalchemy import select, delete

from src.domain.abc.dal import ABCDAL
from src.domain.token.model import Token


class TokenDAL(ABCDAL):
    model = Token

    async def get_by_user_id(self, user_id: UUID) -> Token | None:
        query = select(
            self.model
        ).where(
            self.model.user_id == user_id
        )

        result = (await self.session.execute(query)).scalar_one_or_none()
        return result

    async def delete(self, user_id: UUID):
        query = delete(
            self.model
        ).where(
            self.model.user_id == user_id
        )
        await self.session.execute(query)
