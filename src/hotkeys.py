# -*- coding: utf-8 -*-
"""
Менеджер глобальных горячих клавиш
Обрабатывает системные горячие клавиши
"""

import keyboard
from PyQt5.QtCore import QObject, pyqtSignal
from src.config import HOTKEY_TOGGLE, HOTKEY_CLEAR, HOTKEY_EXIT


class HotkeyManager(QObject):
    """Менеджер глобальных горячих клавиш"""
    
    # Сигналы для различных действий
    toggle_requested = pyqtSignal()
    clear_requested = pyqtSignal()
    exit_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.registered = False
    
    def register_hotkeys(self) -> bool:
        """
        Зарегистрировать все горячие клавиши
        
        Returns:
            bool: True если регистрация успешна, False в случае ошибки
        """
        if self.registered:
            return True
        
        try:
            # Регистрируем горячие клавиши
            keyboard.add_hotkey(HOTKEY_TOGGLE, self.on_toggle)
            keyboard.add_hotkey(HOTKEY_CLEAR, self.on_clear)
            keyboard.add_hotkey(HOTKEY_EXIT, self.on_exit)
            
            self.registered = True
            print(f'✓ Горячие клавиши зарегистрированы:')
            print(f'  - {HOTKEY_TOGGLE.upper()} - Включить/выключить рисование')
            print(f'  - {HOTKEY_CLEAR.upper()} - Очистить экран')
            print(f'  - {HOTKEY_EXIT.upper()} - Выход')
            return True
        
        except PermissionError:
            print(f'⚠ Недостаточно прав для регистрации горячих клавиш')
            print(f'  Попробуйте запустить приложение от имени администратора')
            print(f'  Приложение будет работать без глобальных горячих клавиш')
            self.registered = False
            return False
        
        except Exception as e:
            print(f'⚠ Ошибка регистрации горячих клавиш: {e}')
            print(f'  Приложение будет работать без глобальных горячих клавиш')
            self.registered = False
            return False
    
    def unregister_hotkeys(self) -> bool:
        """
        Отменить регистрацию горячих клавиш
        
        Returns:
            bool: True если отмена успешна, False в случае ошибки
        """
        if not self.registered:
            return True
        
        try:
            keyboard.remove_hotkey(HOTKEY_TOGGLE)
            keyboard.remove_hotkey(HOTKEY_CLEAR)
            keyboard.remove_hotkey(HOTKEY_EXIT)
            self.registered = False
            print('✓ Горячие клавиши отменены')
            return True
        
        except Exception as e:
            print(f'⚠ Ошибка отмены горячих клавиш: {e}')
            return False
    
    def on_toggle(self):
        """Обработчик переключения режима рисования"""
        self.toggle_requested.emit()
    
    def on_clear(self):
        """Обработчик очистки экрана"""
        self.clear_requested.emit()
    
    def on_exit(self):
        """Обработчик выхода из приложения"""
        self.exit_requested.emit()
