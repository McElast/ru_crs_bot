"""Получение курсов валют к рублю, выбранных пользователем."""
from configs import log_configured
from telegram import Update
from telegram.ext import ContextTypes

logger = log_configured.getLogger(__name__)


async def mine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логика команды /mine."""
    if update.effective_chat is not None:
        message: str = (
            f'mine'
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
    else:
        logger.warning('Не получен ID чата при запросе /sub.')
