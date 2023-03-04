"""Информация о функционале бота."""
from configs import log_configured
from telegram import Update
from telegram.ext import ContextTypes

logger = log_configured.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логика команды /help."""
    if update.effective_chat is not None:
        message: str = (
            'Бот предназначен для отображения курса рубля по отношению к следующим валютам:\n'
            '1. Доллар США (USD)\n'
            '2. Евро (EUR)\n'
            '3. Китайский юань (CNY)\n'
            '4. Белорусский рубль (BYN)\n'
            'На выбранные валюты можно подписаться (в том числе не на все)'
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
    else:
        logger.warning('Не получен ID чата при запросе /help.')
