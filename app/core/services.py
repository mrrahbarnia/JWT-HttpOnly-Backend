import logging

from redis import Redis
from django.conf import settings

from users.models import BaseUser

logger = logging.getLogger('backend')


def connect_redis() -> Redis:
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def register_user(email: str, password: str) -> BaseUser:
    BaseUser.objects.create_user(email=email, password=password)


def set_security_stamp(security_stamp: str) -> None:
    redis_conn: Redis = connect_redis()
    redis_conn.set(
        name=security_stamp,
        value=security_stamp,
        ex=int(settings.SECURITY_STAMP_LIFE_TIME)
    )


def get_security_stamp(security_stamp: str) -> bool:
    redis_conn: Redis = connect_redis()
    if redis_conn.get(name=security_stamp):
        return True
    return False


def check_old_password(*, user: BaseUser, old_password: str) -> bool:
    return user.check_password(old_password)


def set_new_password(*, user: BaseUser, new_password: str) -> None:
    redis_conn: Redis = connect_redis()
    redis_conn.getdel(name=user.security_stamp)
    user.set_password(new_password)
    user.save()