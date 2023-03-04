"""Получение доступных курсов валют."""
from configs import log_configured
from telegram import Update
from telegram.ext import ContextTypes

logger = log_configured.getLogger(__name__)


async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логика команды /courses."""
    if update.effective_chat is not None:
        start_message: str = (
            f'Показываю курс рубля специально для тебя, {update.effective_chat.first_name}.'
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=start_message,
        )
    else:
        logger.warning('Не получен ID чата при запросе /courses.')
