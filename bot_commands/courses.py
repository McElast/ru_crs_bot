"""Получение доступных курсов валют."""
import locale
from datetime import datetime

import requests

from configs import log_configured
from configs.base import API_URL, CURRENCIES
from http import HTTPStatus
from telegram import Update
from telegram.ext import ContextTypes

from exceptions import ServiceException

logger = log_configured.getLogger(__name__)
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))


async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логика команды /courses."""
    if update.effective_chat is not None:
        resp = requests.get(API_URL)
        if resp.status_code != HTTPStatus.OK:
            logger.error(f'Ошибочный ответ от сервиса курса валют: {resp.status_code}')
            raise ServiceException(f'Ошибка ответа от {API_URL}: {resp.text}')

        courses_date: str = datetime.strptime(
            resp.json()['Date'], '%Y-%m-%dT%H:%M:%S%z',
        ).strftime('%d %B, %Y %H:%M')

        bot_courses: dict = {}
        for currency in CURRENCIES:
            api_currency_data = resp.json()['Valute'][currency]
            bot_courses[currency] = (
                f'{api_currency_data["Name"]}({api_currency_data["CharCode"]}) = '
                f'{api_currency_data["Value"]:.2f}\n'
            )
        header: str = f'Актуальный курс валют на дату: {courses_date}.'
        message: str = (
            f'{header}\n'
            f'{"=" * len(header)}\n'
            f'{"".join(str(cur_data) for cur_data in bot_courses.values())}'
            f'{"=" * len(header)}'
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
    else:
        logger.warning('Не получен ID чата при запросе /courses.')
