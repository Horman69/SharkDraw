# -*- coding: utf-8 -*-
"""
Утилиты для работы с ресурсами в PyInstaller
"""

import os
import sys
from pathlib import Path


def get_resource_path(relative_path: str) -> str:
    """
    Получить абсолютный путь к ресурсу
    Работает как в режиме разработки, так и в скомпилированном .exe
    
    Args:
        relative_path: Относительный путь к ресурсу (например, 'assets/icons/pen.svg')
    
    Returns:
        Абсолютный путь к ресурсу
    """
    try:
        # PyInstaller создаёт временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Режим разработки - используем текущую директорию
        base_path = Path(__file__).parent.parent
    
    return os.path.join(base_path, relative_path)
