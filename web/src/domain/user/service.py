from uuid import UUID

from fastapi_mail import MessageSchema, FastMail, MessageType
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse

from src.api.auth.dto import SignUpDTO, SignUpResponse, SignInDTO
from src.config.mail import MAIL_CONFIG
from src.config.web import WEB_CONFIG
from src.domain.mail.sign_up import build_sign_up_mail
from src.domain.user.dal import UserDAL
from src.domain.user.exception import EMAIL_ALREADY_EXISTS, USERNAME_ALREADY_EXISTS, USER_NOT_FOUND, \
    USER_ALREADY_CONFIRMED, USER_DISABLED, USER_UNCONFIRMED
from src.domain.auth.exception import INVALID_CREDENTIALS
from src.domain.user.model import User


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


async def email_accept(session: AsyncSession, user_id: UUID) -> HTMLResponse:
    user = await UserDAL(session).get_by_id(user_id)
    if user is None:
        raise USER_NOT_FOUND

    is_confirmed = await UserDAL(session).check_user_confirmed(user_id)
    if is_confirmed is True:
        raise USER_ALREADY_CONFIRMED

    is_enabled = await UserDAL(session).check_user_enabled(user_id)
    if is_enabled is False:
        raise USER_DISABLED

    await UserDAL(session).confirm_user(user_id)

    return HTMLResponse(
        f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Почта подтверждена</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="d-flex justify-content-center align-items-center" style="height: 100vh; background-color: #f4f4f4;">

    <div class="text-center">
        <h1 class="text-success mb-4">Почта подтверждена</h1>
        <p>
            <a href="{WEB_CONFIG.url}">
                <button class="btn btn-success btn-lg">Вернуться на сайт</button>
            </a>
        </p>
    </div>

    <!-- Bootstrap JS, Popper.js, and jQuery -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

</body>
</html>
        """
    )


async def validate_credentials(session: AsyncSession, body: SignInDTO) -> User:
    user_dal = UserDAL(session)

    credentials_valid = await user_dal.check_credentials(body.username, body.password)
    if credentials_valid is False:
        raise INVALID_CREDENTIALS

    user = await user_dal.get_by_username(body.username)
    if user is None:
        raise USER_NOT_FOUND

    if user.is_confirmed is False:
        raise USER_UNCONFIRMED

    if user.is_enabled is False:
        raise USER_DISABLED

    return user


