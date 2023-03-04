"""Инициализатор команд бота."""
from .courses import courses
from .help import help
from .mine import sub, unsub
from .start import start

__all__ = ('courses', 'help', 'start', 'sub', 'unsub')
