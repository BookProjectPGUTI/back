from uuid import UUID

from sqlalchemy import delete

from src.domain.abc.dal import ABCDAL
from src.domain.token.model import Token


class TokenDAL(ABCDAL[Token]):
    async def delete(self, user_id: UUID):
        query = delete(
            self.model
        ).where(
            self.model.user_id == user_id
        )
        await self.session.execute(query)
