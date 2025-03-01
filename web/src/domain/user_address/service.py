from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.dto import UserAddressCreateDTO
from src.domain.auth.dto import AccessTokenDTO
from src.domain.user_address.dal import UserAddressDAL
from src.domain.user_address.dto import UserAddressDTO
from src.domain.user_address.model import UserAddress


async def create_user_address(
        session: AsyncSession,
        user: AccessTokenDTO,
        body: UserAddressCreateDTO
) -> UserAddressDTO:
    user_address = await UserAddressDAL(session).insert(
        {
            UserAddress.user_id.key: user.sub,
            **body.model_dump()
        },
        return_value=True
    )
    return UserAddressDTO.model_validate(user_address)
