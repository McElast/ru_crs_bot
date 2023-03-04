"""Кастомные классы обработки ошибок."""


class APIException(Exception):
    """Ошибки в работе API."""

    ...


class ServiceException(Exception):
    """Ошибки в работе сервиса курса валют."""

    ...
