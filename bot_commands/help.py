"""Информация о функционале бота."""
from configs import log_configured
from telegram import Update
from telegram.ext import ContextTypes

logger = log_configured.getLogger(__name__)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логика команды /help."""
    if update.effective_chat is not None:
        message: str = (
            f'Бот предназначен для отображения курса рубля по отношению к следующим валютам:\n'
            f'1. Доллар США (USD)\n'
            f'2. Евро (EUR)\n'
            f'3. Китайский юань (CNY)\n'
            f'4. Белорусский рубль (BYN)'
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
    else:
        logger.warning('Не получен ID чата при запросе /help.')
