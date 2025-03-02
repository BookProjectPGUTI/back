from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.dto import UserAddressCreateDTO, UserAddressResponse
from src.domain.auth.dto import AccessTokenDTO
from src.domain.user_address.dal import UserAddressDAL
from src.domain.user_address.dto import UserAddressDTO
from src.domain.user_address.exception import USER_ADDRESS_NOT_FOUND
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


async def get_user_addresses(
        session: AsyncSession,
        user: AccessTokenDTO,
) -> UserAddressResponse:
    addresses = await UserAddressDAL(session).get_many_by_filter(
        {UserAddress.user_id.key: user.sub}
    )
    return UserAddressResponse(
        addresses=addresses
    )


async def update_user_address(
        session: AsyncSession,
        user: AccessTokenDTO,
        user_address_id: UUID,
        body: UserAddressCreateDTO,
):
    user_address = await UserAddressDAL(session).get_by_filter(id=user_address_id)
    if user_address is None:
        raise USER_ADDRESS_NOT_FOUND

    await UserAddressDAL(session).update(
        {
            UserAddress.id.key: user_address_id,
            UserAddress.user_id.key: user.sub,
            **body.model_dump()
        },
    )
