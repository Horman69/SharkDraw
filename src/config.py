# -*- coding: utf-8 -*-
"""
Конфигурация приложения PaintPro
Содержит константы, настройки и перечисления
"""

from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class ToolType(Enum):
    """Типы инструментов для рисования"""
    PEN = "pen"              # Карандаш
    LINE = "line"            # Линия
    RECTANGLE = "rectangle"  # Прямоугольник
    CIRCLE = "circle"        # Круг
    ARROW = "arrow"          # Стрелка
    ERASER = "eraser"        # Ластик


# Палитра цветов
COLORS = {
    'Красный': QColor(255, 59, 48),
    'Синий': QColor(0, 122, 255),
    'Зелёный': QColor(52, 199, 89),
    'Жёлтый': QColor(255, 204, 0),
    'Чёрный': QColor(0, 0, 0),
    'Белый': QColor(255, 255, 255),
    'Оранжевый': QColor(255, 149, 0),
    'Фиолетовый': QColor(175, 82, 222),
}

# Настройки по умолчанию
DEFAULT_COLOR = QColor(255, 59, 48)  # Красный
DEFAULT_LINE_WIDTH = 3
MIN_LINE_WIDTH = 1
MAX_LINE_WIDTH = 10

# Горячие клавиши
HOTKEY_TOGGLE = 'ctrl+d'      # Включить/выключить режим рисования
HOTKEY_CLEAR = 'ctrl+shift+c' # Очистить экран
HOTKEY_EXIT = 'esc'           # Выход из приложения

# Настройки окна
WINDOW_OPACITY = 1.0          # Непрозрачность окна (1.0 = полностью непрозрачно)
TOOLBAR_WIDTH = 80            # Ширина панели инструментов
TOOLBAR_PADDING = 10          # Отступы в панели инструментов

# Настройки производительности
MAX_DRAWINGS = 1000           # Максимальное количество рисунков (для предотвращения утечки памяти)
DEBUG_MODE = False            # Режим отладки (выводить подробные логи)

# Настройки рисования
ERASER_RADIUS_MULTIPLIER = 3  # Множитель радиуса ластика относительно толщины линии
OVERLAY_OPACITY = 40          # Прозрачность оверлея при рисовании (0-255)
MOUSE_LOG_INTERVAL = 20       # Интервал логирования движения мыши (в пикселях)

# ============================================================================
# SHARKDRAW BRANDING
# ============================================================================

APP_NAME = 'SharkDraw'
APP_SLOGAN = 'Bite into your ideas'

# SharkDraw Color Palette
SHARK_GRAY = QColor(107, 123, 140)      # #6B7B8C - основной серый
BANANA_YELLOW = QColor(255, 217, 61)    # #FFD93D - акцентный желтый
DEEP_OCEAN = QColor(26, 35, 50)         # #1A2332 - темный фон
WHITE_TEETH = QColor(248, 249, 250)     # #F8F9FA - светлый текст

# Glassmorphism Settings
GLASS_OPACITY = 0.85          # Прозрачность glassmorphism панели
GLASS_BLUR = 10               # Радиус размытия
GLASS_BORDER_OPACITY = 0.1    # Прозрачность границы

# Sound Settings
ENABLE_SOUNDS = False         # Звуки (пока отключены)
SOUND_VOLUME = 0.5            # Громкость звуков (0.0 - 1.0)

