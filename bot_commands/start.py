"""Стартовая команда бота."""
from telegram import Update
from telegram.ext import ContextTypes

from configs import log_configured

logger = log_configured.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логика команды /start."""
    if update.effective_chat is not None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Показываю курс рубля.',
        )
    else:
        logger.warning('Не получен ID чата при запросе /start.')
    print(322113, update.effective_chat)
