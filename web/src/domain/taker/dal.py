from uuid import UUID

from sqlalchemy import select, func

from src.domain.abc.dal import ABCDAL
from src.domain.maker.model import Maker
from src.domain.taker.model import Taker


class TakerDAL(ABCDAL[Taker]):
    async def get_success_exchanges_count(self, user_id: UUID) -> int:
        success_taker = select(
            func.count(self.model.id),
        ).where(
            self.model.user_id == user_id,
            self.model.is_received.is_(True)
        ).scalar_subquery()

        success_maker = select(
            func.count(Maker.id),
        ).where(
            Maker.user_id == user_id,
            Maker.is_received.is_(True)
        ).scalar_subquery()

        query = select(
            func.coalesce(success_taker, 0) + func.coalesce(success_maker, 0)
        )

        result = await self.session.execute(query)
        return result.one()[0]
