# -*- coding: utf-8 -*-
"""
Скрипт для создания установочного пакета SharkDraw
Использует PyInstaller для создания standalone .exe файла
"""

import os
import shutil
from pathlib import Path

def create_installer():
    """Создать установочный пакет"""
    
    print('=' * 60)
    print('🎨 Создание установочного пакета SharkDraw')
    print('=' * 60)
    print()
    
    # Проверяем наличие PyInstaller
    try:
        import PyInstaller
        print('✓ PyInstaller установлен')
    except ImportError:
        print('❌ PyInstaller не установлен')
        print('\nУстановите командой:')
        print('  python -m pip install pyinstaller')
        return
    
    print('\n📦 Создание .exe файла...')
    print('Это может занять несколько минут...\n')
    
    # Команда для PyInstaller
    cmd = [
        'pyinstaller',
        '--name=SharkDraw',
        '--onefile',  # Один файл
        '--windowed',  # Без консоли
        '--icon=assets/Logo.ico',  # Иконка
        '--add-data=assets;assets',  # Включить assets
        '--add-data=src;src',  # Включить src
        'main.py'
    ]
    
    # Запускаем PyInstaller
    os.system(' '.join(cmd))
    
    print('\n✅ Сборка завершена!')
    print('\n📁 Файлы находятся в:')
    print('  dist/SharkDraw.exe - готовый исполняемый файл')
    print('\n💡 Для распространения:')
    print('  1. Скопируйте SharkDraw.exe из папки dist/')
    print('  2. Отправьте файл другому пользователю')
    print('  3. Пользователь просто запускает .exe файл')

if __name__ == '__main__':
    create_installer()
