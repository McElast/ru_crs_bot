"""Получение доступных курсов валют."""
from datetime import datetime

from configs import log_configured
from configs.base import CURRENCIES
from requests import Response
from telegram import Update
from telegram.ext import ContextTypes
from utils.handlers import make_request

logger = log_configured.getLogger(__name__)


async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логика команды /courses."""
    if update.effective_chat is not None:
        resp: Response = make_request()

        courses_date: str = datetime.strptime(
            resp.json()['Date'], '%Y-%m-%dT%H:%M:%S%z',
        ).strftime('%d %B, %Y %H:%M')

        bot_courses: dict = {}
        for currency in CURRENCIES:
            api_currency_data: dict = resp.json()['Valute'][currency]
            bot_courses[currency] = (
                f'{api_currency_data["Name"]}({api_currency_data["CharCode"]}) = '
                f'{api_currency_data["Value"]:.2f}\n'
            )
        message: str = ''
        if not context.args:
            header: str = f'Актуальный курс валют на дату: {courses_date}.'
            message = (
                f'{header}\n'
                f'{"=" * len(header)}\n'
                f'{"".join(str(cur_data) for cur_data in bot_courses.values())}'
                f'{"=" * len(header)}'
            )
        else:
            for param in context.args:
                if param.upper() in CURRENCIES:
                    message += f'{bot_courses[param.upper()]}'
                else:
                    logger.warning(f'Запрошена недопустимая валюта {param.upper()}')

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
    else:
        logger.warning('Не получен ID чата при запросе /courses.')
