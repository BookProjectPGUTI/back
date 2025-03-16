import typing
import uuid

from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from sqlalchemy import func, UUID, VARCHAR, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.abc.model import ABCTimestampModel


if typing.TYPE_CHECKING:
    from src.domain.user.model import User


def _user():
    from src.domain.user.model import User

    return User


class UserAddress(ABCTimestampModel):
    __tablename__ = 'user_address'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=func.gen_random_uuid(), comment='Уникальный ID'
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey(_user().id), nullable=False, comment='ID владельца книги'
    )

    mail_index: Mapped[str] = mapped_column(
        VARCHAR(6), nullable=False, comment='Почтовый индекс'
    )

    city: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, comment='Название города'
    )

    street: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, comment='Название улицы'
    )

    house: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=True, comment='Номер дома'
    )

    build: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=True, comment='Номер строения'
    )

    apartment: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, comment='Номер квартиры'
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, comment='Активность адреса'
    )

    user: Mapped['User'] = relationship()


inactive_else_user_address_function = PGFunction(
    schema="public",
    signature="inactive_else_user_address_function()",
    definition=f"""
    RETURNS TRIGGER AS $$
    DECLARE
        active_count INT;
    BEGIN
        IF OLD.is_active = TRUE AND NEW.is_active = TRUE THEN
            RETURN NEW;
        END IF;

        SELECT COUNT(*) INTO active_count 
        FROM public.{UserAddress.__tablename__} 
        WHERE public.{UserAddress.__tablename__}.is_active = TRUE AND public.{UserAddress.__tablename__}.id <> NEW.id;

        IF NEW.is_active = TRUE THEN
            UPDATE public.{UserAddress.__tablename__}
            SET is_active = FALSE
            WHERE public.{UserAddress.__tablename__}.is_active = TRUE AND public.{UserAddress.__tablename__}.id <> NEW.id;

        ELSE
            IF active_count = 0 THEN
                NEW.is_active := TRUE;
            END IF;
        END IF;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql
    """
)

inactive_else_user_address_trigger = PGTrigger(
    schema="public",
    signature="inactive_else_user_address_trigger",
    on_entity=f"{UserAddress.__tablename__}",
    definition=f"""
        BEFORE INSERT OR UPDATE ON {UserAddress.__tablename__}
        FOR EACH ROW
        WHEN (pg_trigger_depth() = 0)
        EXECUTE FUNCTION public.inactive_else_user_address_function()
    """
)
