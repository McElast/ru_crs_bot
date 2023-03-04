"""Обработчики параметров."""
import os

from exceptions import APIException


def get_token(key: str) -> str:
    """Проверяем наличие токена."""
    token: str | None = os.getenv(key)
    if token is not None:
        return token
    raise APIException('Не передан токен для доступа к боту.')
