"""Обработчики параметров."""
import os

from exceptions import APIException
from telegram.ext import ContextTypes


def get_token(key: str) -> str:
    """Проверяем наличие токена."""
    token: str | None = os.getenv(key)
    if token is not None:
        return token
    raise APIException('Не передан токен для доступа к боту.')


async def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Удалить подписку, если она уже существовала."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def send_subscription(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляем уведомление по подписанным валютам."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f'Прошло {job.data} секунд.')
