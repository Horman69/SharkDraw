# -*- coding: utf-8 -*-
"""
Менеджер звуковых эффектов для SharkDraw
Использует winsound (встроенный модуль Windows) для воспроизведения звуков
"""

import os
import sys
from pathlib import Path


class SoundManager:
    """Управление звуковыми эффектами приложения"""
    
    def __init__(self, sounds_dir: str = None):
        """
        Инициализация менеджера звуков
        
        Args:
            sounds_dir: Путь к папке со звуками (по умолчанию assets/sounds)
        """
        self.enabled = False
        self.sounds = {}
        
        # Определяем путь к папке со звуками
        if sounds_dir is None:
            # Получаем путь к корневой папке проекта
            project_root = Path(__file__).parent.parent
            sounds_dir = project_root / 'assets' / 'sounds'
        else:
            sounds_dir = Path(sounds_dir)
        
        self.sounds_dir = sounds_dir
        
        # Проверяем, что мы на Windows
        if sys.platform == 'win32':
            try:
                import winsound
                self.winsound = winsound
                self.enabled = True
                print('✓ Звуковая система инициализирована (winsound)')
            except ImportError:
                print('⚠ Модуль winsound не доступен')
                self.enabled = False
                return
        else:
            print('⚠ Звуки поддерживаются только на Windows')
            self.enabled = False
            return
        
        # Загружаем звуковые файлы
        self._load_sounds()
    
    def _load_sounds(self):
        """Загрузка звуковых файлов из папки"""
        if not self.enabled:
            return
        
        if not self.sounds_dir.exists():
            print(f'⚠ Папка со звуками не найдена: {self.sounds_dir}')
            return
        
        # Список звуковых файлов для загрузки (только WAV для winsound)
        sound_files = {
            'startup': ['startup.wav'],
            'click': ['click.wav'],
            'close': ['close.wav']
        }
        
        # Проверяем наличие каждого звука
        for sound_name, possible_files in sound_files.items():
            loaded = False
            for filename in possible_files:
                sound_path = self.sounds_dir / filename
                if sound_path.exists():
                    self.sounds[sound_name] = str(sound_path)
                    print(f'✓ Найден звук: {sound_name} ({filename})')
                    loaded = True
                    break
            
            if not loaded:
                print(f'⚠ Звук "{sound_name}" не найден в {self.sounds_dir}')
    
    def play_startup(self):
        """Воспроизвести звук запуска приложения"""
        self._play_sound('startup')
    
    def play_click(self):
        """Воспроизвести звук клика по кнопке"""
        self._play_sound('click')
    
    def play_close(self):
        """Воспроизвести звук закрытия приложения"""
        self._play_sound('close', wait=True)
    
    def _play_sound(self, sound_name: str, wait: bool = False):
        """
        Воспроизвести звук по имени
        
        Args:
            sound_name: Название звука ('startup', 'click', 'close')
            wait: Ждать завершения воспроизведения (для звука закрытия)
        """
        if not self.enabled:
            return
        
        sound_path = self.sounds.get(sound_name)
        if sound_path:
            try:
                # SND_ASYNC - асинхронное воспроизведение (не блокирует)
                # SND_SYNC - синхронное воспроизведение (ждёт завершения)
                # SND_NODEFAULT - не воспроизводить системный звук при ошибке
                flags = self.winsound.SND_FILENAME | self.winsound.SND_NODEFAULT
                
                if wait:
                    flags |= self.winsound.SND_SYNC
                else:
                    flags |= self.winsound.SND_ASYNC
                
                self.winsound.PlaySound(sound_path, flags)
                    
            except Exception as e:
                # Тихо игнорируем ошибки воспроизведения
                pass
    
    def set_volume(self, volume: float):
        """
        Установить громкость всех звуков
        
        Args:
            volume: Громкость от 0.0 до 1.0
        """
        # winsound не поддерживает управление громкостью
        # Громкость контролируется системными настройками Windows
        pass
    
    def cleanup(self):
        """Освобождение ресурсов звуковой системы"""
        if self.enabled:
            try:
                # Останавливаем все звуки
                self.winsound.PlaySound(None, self.winsound.SND_PURGE)
                print('✓ Звуковая система остановлена')
            except Exception as e:
                print(f'⚠ Ошибка при остановке звуковой системы: {e}')
