from fastapi_mail import MessageSchema, FastMail, MessageType
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.dto import SignUpDTO, SignUpResponse
from src.config.mail import MAIL_CONFIG
from src.domain.mail.sign_up import build_sign_up_mail
from src.domain.user.dal import UserDAL
from src.domain.user.exception import EMAIL_ALREADY_EXISTS, USERNAME_ALREADY_EXISTS


async def sign_up(session: AsyncSession, body: SignUpDTO) -> SignUpResponse:
    email_exists = await UserDAL(session).check_email_exists(body.email)
    if email_exists is True:
        raise EMAIL_ALREADY_EXISTS

    username_exists = await UserDAL(session).check_username_exists(body.username)
    if username_exists is True:
        raise USERNAME_ALREADY_EXISTS

    user_id = await UserDAL(session).insert(body.model_dump())

    html = build_sign_up_mail(user_id)

    message = MessageSchema(
        subject='Регистрация BookProject',
        recipients=[body.email],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(MAIL_CONFIG)
    await fm.send_message(message)

    return SignUpResponse()
