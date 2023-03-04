"""Получение курсов валют к рублю, выбранных пользователем."""
from configs import log_configured
from configs.base import CURRENCIES
from exceptions import ServiceException
from telegram import Update
from telegram.ext import ContextTypes
from utils.handlers import remove_job_if_exists, send_subscription

logger = log_configured.getLogger(__name__)


async def sub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логика команды /sub."""
    if update.effective_chat is not None:
        message: str = (
            'Можно подписаться на следующие валюты:\n'
            f'{" ".join((cur for cur in CURRENCIES))}\n'
            'Делается так: /sub 10 USD CNY\n'
            'Первый параметр - время в секундах, остальные - валюты для подписки\n'
            'Минимально нужно указать время и хотя бы 1 валюту, иначе не сработает'
        )

        if context.args and context.args[0].isnumeric():
            if int(context.args[0]) <= 5:
                logger.warning('Первый параметр в подписке меньше или равен 5 сек.')
                raise ServiceException(
                    f'Установите периодичность подписки числом,  большим 5 сек, а не {context.args[0]}',
                )
            subbed_curs: list = []
            for param in context.args[1:]:
                if param.upper() in CURRENCIES:
                    subbed_curs.append(param.upper())
                else:
                    logger.warning(f'Игнорируем недоступную валюту для рассылки: {param.upper()}')
            message = (
                f'Подписан на валюты = {*subbed_curs, } =.\nРассылка раз в {context.args[0]} секунд.'
            )

            await remove_job_if_exists(str(update.effective_chat.id), context)

            context.job_queue.run_repeating(  # type: ignore
                send_subscription, int(context.args[0]),
                chat_id=update.effective_chat.id,
                name=str(update.effective_chat.id),
                data=[int(context.args[0]), subbed_curs],
            )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
    else:
        logger.warning('Не получен ID чата при запросе /sub.')


async def unsub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отменить подписку."""
    if update.effective_chat is not None:
        job_removed = await remove_job_if_exists(str(update.effective_chat.id), context)
        message = 'Подписка отменена' if job_removed else 'Подписки не было. Отменять нечего.'
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
    else:
        logger.warning('В unsub не передан effective_chat.')
