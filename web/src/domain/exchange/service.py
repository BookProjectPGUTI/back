from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.auth.dto import AccessTokenDTO
from src.domain.maker.dal import MakerDAL
from src.domain.maker.exception import MAKER_ALREADY_EXISTS
from src.domain.maker.model import Maker
from src.domain.taker.dal import TakerDAL
from src.domain.taker.exception import TAKER_ALREADY_EXISTS
from src.domain.taker.model import Taker


async def validate_current_exchange(session: AsyncSession, user: AccessTokenDTO):
    maker_dal = MakerDAL(session)
    taker_dal = TakerDAL(session)

    active_maker = await maker_dal.get_by_filter(
        {
            Maker.user_id.key: user.sub,
            Maker.is_received.key: False,
        }
    )
    if active_maker is not None:
        raise MAKER_ALREADY_EXISTS

    active_taker = await taker_dal.get_by_filter(
        {
            Taker.user_id.key: user.sub,
            Taker.is_received.key: False,
        }
    )
    if active_taker is not None:
        raise TAKER_ALREADY_EXISTS
