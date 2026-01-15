# -*- coding: utf-8 -*-
"""
PaintPro - Приложение для рисования поверх экрана
Главный файл приложения
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.canvas import TransparentCanvas
from src.toolbar import Toolbar
from src.hotkeys import HotkeyManager
from src.config import ToolType
from src.sound_manager import SoundManager


class PaintProApp:
    """Главное приложение PaintPro"""
    
    def __init__(self):
        """Инициализация приложения"""
        self.app = QApplication(sys.argv)
        self.app.setApplicationName('PaintPro')
        
        # Создаём компоненты
        self.sound_manager = SoundManager()
        self.canvas = TransparentCanvas()
        self.toolbar = Toolbar(self.sound_manager)
        self.hotkey_manager = HotkeyManager()
        
        # Состояние приложения
        self.drawing_enabled = False
        
        # Подключаем сигналы
        self.connect_signals()
        
        # Регистрируем горячие клавиши
        self.hotkey_manager.register_hotkeys()
        
        # Показываем компоненты
        self.canvas.show()
        self.toolbar.show()
        
        # Передаём холсту область панели инструментов
        self.canvas.set_toolbar_rect(self.toolbar.geometry())
        
        # Изначально режим рисования выключен
        self.canvas.disable_drawing()
        
        # Воспроизводим звук запуска
        self.sound_manager.play_startup()
        
        print('✓ PaintPro запущен!')
        print('  Нажмите Ctrl+D для включения режима рисования')
    
    def connect_signals(self):
        """Подключить сигналы между компонентами"""
        # Сигналы от панели инструментов
        self.toolbar.tool_changed.connect(self.on_tool_changed)
        self.toolbar.color_changed.connect(self.on_color_changed)
        self.toolbar.width_changed.connect(self.on_width_changed)
        self.toolbar.clear_requested.connect(self.on_clear_requested)
        self.toolbar.close_requested.connect(self.on_exit_requested)
        self.toolbar.toggle_drawing_requested.connect(self.on_toggle_drawing)  # Новое подключение
        self.toolbar.geometry_changed.connect(self.on_toolbar_moved)  # Отслеживаем перемещение панели
        
        # Сигналы от менеджера горячих клавиш
        self.hotkey_manager.toggle_requested.connect(self.on_toggle_drawing)
        self.hotkey_manager.clear_requested.connect(self.on_clear_requested)
        self.hotkey_manager.exit_requested.connect(self.on_exit_requested)
    
    def on_tool_changed(self, tool_type: ToolType):
        """Обработка смены инструмента"""
        self.canvas.set_tool(tool_type)
        print(f'✓ Инструмент изменён: {tool_type.value}')
    
    def on_color_changed(self, color):
        """Обработка смены цвета"""
        self.canvas.set_color(color)
        print(f'✓ Цвет изменён: {color.name()}')
    
    def on_width_changed(self, width: int):
        """Обработка смены толщины линии"""
        self.canvas.set_width(width)
        print(f'✓ Толщина изменена: {width} px')
    
    def on_clear_requested(self):
        """Обработка запроса на очистку экрана"""
        self.canvas.clear_canvas()
        print('✓ Экран очищен')
    
    def on_toggle_drawing(self):
        """Переключение режима рисования"""
        self.drawing_enabled = not self.drawing_enabled
        
        if self.drawing_enabled:
            self.canvas.enable_drawing()
            print('✓ Режим рисования ВКЛЮЧЕН')
        else:
            self.canvas.disable_drawing()
            print('✓ Режим рисования ВЫКЛЮЧЕН')
        
        # Синхронизируем состояние кнопки на панели
        self.toolbar.update_drawing_mode(self.drawing_enabled)
    
    def on_toolbar_moved(self):
        """Обработка перемещения панели инструментов"""
        self.canvas.set_toolbar_rect(self.toolbar.geometry())
    
    def on_exit_requested(self):
        """Обработка запроса на выход"""
        print('✓ Выход из приложения...')
        
        # Воспроизводим звук закрытия
        self.sound_manager.play_close()
        
        self.cleanup()
        self.app.quit()
    
    def cleanup(self):
        """Очистка ресурсов перед выходом"""
        self.hotkey_manager.unregister_hotkeys()
        self.sound_manager.cleanup()
        print('✓ Ресурсы освобождены')
    
    def run(self):
        """Запуск приложения"""
        try:
            return self.app.exec_()
        except KeyboardInterrupt:
            print('\n✓ Прервано пользователем')
            self.cleanup()
            return 0


def main():
    """Точка входа в приложение"""
    print('=' * 50)
    print('🎨 PaintPro - Рисование поверх экрана')
    print('=' * 50)
    print()
    
    # Создаём и запускаем приложение
    app = PaintProApp()
    sys.exit(app.run())


if __name__ == '__main__':
    main()
