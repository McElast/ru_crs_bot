"""Инициализатор команд бота."""
from .courses import courses
from .help import help_command
from .mine import sub, unsub
from .start import start

__all__ = ('courses', 'help_command', 'start', 'sub', 'unsub')
