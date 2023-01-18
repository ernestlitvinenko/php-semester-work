import typing

from loguru import logger

from models import UserSchema
from models.mongo_models import Items
from models.mongo_models.user import User, UserExistsException
from fastapi import HTTPException


class ListItemsChecks:
    @staticmethod
    def is_admin(user: User):
        return user.is_admin


class ListItemsTemplates:
    # todo подумай как шаблоны распределить
    user: User = None

    def set_user(self, user: User):
        self.user = user


async def retrieving_user_with_cred(**kwargs) -> User:
    pwd = kwargs.pop('password', None)
    user = User.objects(**kwargs).first()
    log_str = [f"{key}='{val}'" for key, val in kwargs.items()]
    log_str = ", ".join(log_str)
    logger.debug(f"User with {log_str} is {'not' if user is None else ''} founded")

    if not user:
        raise HTTPException(status_code=403, detail=f"User with {log_str} not founded")

    if pwd:
        if not user.check_pwd(pwd):
            log_str = f"Incorrect password for {log_str}"
            logger.debug(log_str)
            raise HTTPException(status_code=401, detail=log_str)

    return user


async def create_user(user: UserSchema) -> User:
    try:
        user = await User.create_user(**user.dict())
        logger.debug(f"User {user.username} was created")

    except UserExistsException as exc:
        logger.debug(str(exc))
        raise HTTPException(status_code=403, detail=str(exc))
    return user


async def list_items(subject, **kwargs) -> list[Items]:
    user = await retrieving_user_with_cred(id=subject['user_id'])
    return list(Items.objects(**kwargs))

