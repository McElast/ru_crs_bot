"""Стартовая команда бота."""
from configs import log_configured
from telegram import Update
from telegram.ext import ContextTypes

logger = log_configured.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логика команды /start."""
    if update.effective_chat is not None:
        message: str = (
            f'Показываю курс рубля специально для тебя, {update.effective_chat.first_name}.'
            '\n======<b>Доступные команды</b>======\n'
            '- /start - приветственная информация\n'
            '- /help - информация о функционале бота\n'
            '- /courses - курсы всех валют к рублю\n'
            '- /sub - подписаться на рассылку (с периодичностью в секундах, по выбранным валютам)\n'
            '- /unsub - отписаться от рассылки'
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message, parse_mode='HTML',
        )
    else:
        logger.warning('Не получен ID чата при запросе /start.')
