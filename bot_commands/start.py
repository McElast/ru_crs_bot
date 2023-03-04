"""Стартовая команда бота."""
from configs import log_configured
from telegram import Update
from telegram.ext import ContextTypes

logger = log_configured.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логика команды /start."""
    if update.effective_chat is not None:
        start_message: str = (
            f'Показываю курс рубля специально для тебя, {update.effective_chat.first_name}.'
            '\n======Доступные команды======\n'
            '- /start - приветственная информация\n'
            '- /courses - доступные курсы валют\n'
            '- /mine - показать мои курсы валют'
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=start_message,
        )
    else:
        logger.warning('Не получен ID чата при запросе /start.')
