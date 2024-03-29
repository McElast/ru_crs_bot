"""Обработчики параметров."""
import os
from http import HTTPStatus

import requests

from configs import log_configured
from configs.base import API_URL
from exceptions import APIException, ServiceException
from requests import Response
from telegram.ext import ContextTypes, Job

logger = log_configured.getLogger(__name__)


def get_token(key: str) -> str:
    """Проверяем наличие токена."""
    token: str | None = os.getenv(key)
    if token is not None:
        return token
    raise APIException('Не передан токен для доступа к боту.')


async def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Удалить подписку, если она уже существовала."""
    current_jobs: tuple = context.job_queue.get_jobs_by_name(name)  # type: ignore
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def send_subscription(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляем уведомление по подписанным валютам."""
    job: Job | None = context.job
    resp: dict = make_request().json()
    message: str = f'Прошло {job.data[0]} секунд.'  # type: ignore
    for currency in job.data[1]:  # type: ignore
        message += f'\n{resp["Valute"][currency]["CharCode"]} = {resp["Valute"][currency]["Value"]:.3f}'
    await context.bot.send_message(str(job.chat_id), text=message)  # type: ignore


def make_request(url: str = API_URL) -> Response:
    """Получение ответа от АПИ валют."""
    resp: Response = requests.get(url)
    if resp.status_code != HTTPStatus.OK:
        logger.error(f'Ошибочный ответ от сервиса курса валют: {resp.status_code}')
        raise ServiceException(f'Ошибка ответа от {API_URL}: {resp.text}')
    return resp
