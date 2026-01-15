# -*- coding: utf-8 -*-
"""
SharkDraw Toolbar
Современная панель инструментов с glassmorphism эффектами
"""

import os
from typing import Optional
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QSlider, QLabel, QButtonGroup, QGridLayout, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QColor, QPalette, QMouseEvent, QPixmap
from src.config import (ToolType, COLORS, MIN_LINE_WIDTH, MAX_LINE_WIDTH, DEFAULT_LINE_WIDTH,
                        APP_NAME, SHARK_GRAY, BANANA_YELLOW, DEEP_OCEAN, WHITE_TEETH)
from src import styles
from src.clickable_slider import ClickableSlider
from src.resource_path import get_resource_path


class Toolbar(QWidget):
    """Панель инструментов с кнопками и настройками"""
    
    # Сигналы для связи с основным приложением
    tool_changed = pyqtSignal(ToolType)
    color_changed = pyqtSignal(QColor)
    width_changed = pyqtSignal(int)
    clear_requested = pyqtSignal()
    close_requested = pyqtSignal()
    toggle_drawing_requested = pyqtSignal()  # Новый сигнал для переключения режима рисования
    geometry_changed = pyqtSignal()  # Сигнал при изменении позиции панели
    
    def __init__(self, sound_manager=None):
        super().__init__()
        self.sound_manager = sound_manager
        self.init_ui()
        
        # Для перетаскивания панели
        self.dragging = False
        self.drag_position = QPoint()
        
        # Состояние режима рисования
        self.drawing_mode = False
    
    def init_ui(self) -> None:
        """Инициализация интерфейса панели"""
        self.setWindowTitle(APP_NAME)
        self.setObjectName('toolbar')
        
        # Окно поверх всех, без рамки
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        
        # Применяем glassmorphism стиль к панели (shark theme)
        self.setStyleSheet("""
            QWidget#toolbar {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(26, 35, 50, 180),
                    stop:1 rgba(20, 28, 40, 160)
                );
                border: 1px solid #666;
                border-radius: 16px;
            }
        """)
        
        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)
        
        # ========== HEADER ==========
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Логотип
        logo_label = QLabel()
        logo_label.setObjectName('header_logo')
        logo_label.setFixedSize(32, 32)
        logo_path = get_resource_path('assets/logo.ico')
        if os.path.exists(logo_path):
            from PyQt5.QtGui import QPainter, QBrush, QPainterPath
            from PyQt5.QtCore import QRectF
            
            # Загружаем и масштабируем изображение
            original_pixmap = QPixmap(logo_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Создаем круглую маску
            rounded_pixmap = QPixmap(32, 32)
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Создаем круглый путь
            path = QPainterPath()
            path.addEllipse(QRectF(0, 0, 32, 32))
            
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, original_pixmap)
            painter.end()
            
            logo_label.setPixmap(rounded_pixmap)
        else:
            logo_label.setText('🦈')
            logo_label.setStyleSheet('font-size: 24px;')
        
        # Название
        title_label = QLabel(APP_NAME)
        title_label.setObjectName('header_title')
        title_label.setStyleSheet(styles.HEADER_STYLE)
        
        # Кнопка закрытия
        close_btn = QPushButton('✕')
        close_btn.setObjectName('close_btn')
        close_btn.setStyleSheet(styles.HEADER_STYLE)
        close_btn.clicked.connect(lambda: (self._play_click(), self.close_requested.emit()))
        close_btn.setCursor(Qt.PointingHandCursor)
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        main_layout.addLayout(header_layout)
        
        # Разделитель
        main_layout.addWidget(self.create_separator())
        
        
        # ========== TOGGLE BUTTON ==========
        self.toggle_btn = QPushButton('ВКЛЮЧИТЬ\nРИСОВАНИЕ')
        self.toggle_btn.setObjectName('toggle_btn')
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setStyleSheet(styles.TOGGLE_BUTTON_STYLE)
        self.toggle_btn.clicked.connect(self.on_toggle_drawing)
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        main_layout.addWidget(self.toggle_btn)
        
        # ========== CLEAR BUTTON ==========
        clear_btn = QPushButton('ОЧИСТИТЬ ЭКРАН')
        clear_btn.setObjectName('clear_btn')
        clear_btn.setStyleSheet(styles.CLEAR_BUTTON_STYLE)
        clear_btn.clicked.connect(lambda: (self._play_click(), self.clear_requested.emit()))
        clear_btn.setCursor(Qt.PointingHandCursor)
        main_layout.addWidget(clear_btn)
        
        # Разделитель
        main_layout.addWidget(self.create_separator())
        
        
        # ========== TOOLS SECTION ==========
        tools_label = QLabel('ИНСТРУМЕНТЫ')
        tools_label.setObjectName('section_title')
        tools_label.setStyleSheet(styles.LABEL_STYLE)
        main_layout.addWidget(tools_label)
        
        self.tool_buttons = {}
        self.tool_button_group = QButtonGroup(self)
        
        tools = [
            (ToolType.PEN, 'pen.svg', 'Карандаш'),
            (ToolType.LINE, 'line.svg', 'Линия'),
            (ToolType.RECTANGLE, 'rectangle.svg', 'Прямоугольник'),
            (ToolType.CIRCLE, 'circle.svg', 'Круг'),
            (ToolType.ARROW, 'arrow.svg', 'Стрелка'),
            (ToolType.ERASER, 'eraser.svg', 'Ластик'),
        ]
        
        # Сетка 2x3 для иконок
        tools_grid = QGridLayout()
        tools_grid.setSpacing(6)
        tools_grid.setContentsMargins(0, 0, 0, 0)
        
        for i, (tool_type, icon_file, tooltip) in enumerate(tools):
            btn = self.create_icon_button(icon_file, tooltip, tool_type)
            self.tool_buttons[tool_type] = btn
            self.tool_button_group.addButton(btn)
            row = i // 3
            col = i % 3
            tools_grid.addWidget(btn, row, col)
        
        main_layout.addLayout(tools_grid)
        
        # Карандаш выбран по умолчанию
        self.tool_buttons[ToolType.PEN].setChecked(True)
        
        # Разделитель
        main_layout.addWidget(self.create_separator())
        
        # ========== COLORS SECTION ==========
        colors_label = QLabel('ЦВЕТА')
        colors_label.setObjectName('section_title')
        colors_label.setStyleSheet(styles.LABEL_STYLE)
        main_layout.addWidget(colors_label)
        
        # Сетка цветов 2x4
        colors_grid = QGridLayout()
        colors_grid.setSpacing(8)
        colors_grid.setContentsMargins(0, 0, 0, 0)
        
        self.color_buttons = {}
        self.color_button_group = QButtonGroup(self)
        
        row = 0
        col = 0
        for name, color in COLORS.items():
            btn = self.create_color_button(color)
            btn.setToolTip(name)
            self.color_buttons[name] = btn
            self.color_button_group.addButton(btn)
            colors_grid.addWidget(btn, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        main_layout.addLayout(colors_grid)
        
        # Красный выбран по умолчанию
        self.color_buttons['Красный'].setChecked(True)
        
        # Разделитель
        main_layout.addWidget(self.create_separator())
        
        # ========== WIDTH SECTION ==========
        width_label = QLabel('ТОЛЩИНА')
        width_label.setObjectName('section_title')
        width_label.setStyleSheet(styles.LABEL_STYLE)
        main_layout.addWidget(width_label)
        
        self.width_value_label = QLabel(f'{DEFAULT_LINE_WIDTH} px')
        self.width_value_label.setStyleSheet(styles.LABEL_STYLE + ' text-align: center;')
        self.width_value_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.width_value_label)
        
        self.width_slider = ClickableSlider(Qt.Horizontal)
        self.width_slider.setMinimum(MIN_LINE_WIDTH)
        self.width_slider.setMaximum(MAX_LINE_WIDTH)
        self.width_slider.setValue(DEFAULT_LINE_WIDTH)
        self.width_slider.setStyleSheet(styles.SLIDER_STYLE)
        self.width_slider.setCursor(Qt.PointingHandCursor)
        self.width_slider.valueChanged.connect(self.on_width_changed)
        main_layout.addWidget(self.width_slider)
        
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Фиксированная ширина для консистентности на разных мониторах
        self.setFixedWidth(220)
        self.setMaximumHeight(700)
        
        # Позиционируем в правом верхнем углу
        screen = QApplication.desktop().screenGeometry()
        self.move(screen.width() - self.width() - 20, 20)
    
    def create_icon_button(self, icon_file: str, tooltip: str, tool_type: ToolType) -> QPushButton:
        """Создать кнопку инструмента с иконкой"""
        from PyQt5.QtSvg import QSvgRenderer
        from PyQt5.QtGui import QPixmap, QPainter, QIcon
        
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setFixedSize(56, 56)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.PointingHandCursor)
        
        # Загрузка SVG иконки с правильным путём для PyInstaller
        icon_path = get_resource_path(os.path.join('assets', 'icons', icon_file))
        if os.path.exists(icon_path):
            # Создаем QIcon из SVG
            pixmap = QPixmap(24, 24)
            pixmap.fill(Qt.transparent)
            
            renderer = QSvgRenderer(icon_path)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(pixmap.size())
        
        btn.setStyleSheet(styles.ICON_BUTTON_STYLE)
        btn.clicked.connect(lambda: (self._play_click(), self.tool_changed.emit(tool_type)))
        return btn
    
    def create_tool_button(self, name: str, tool_type: ToolType) -> QPushButton:
        """Создать кнопку инструмента"""
        btn = QPushButton(name)
        btn.setCheckable(True)
        btn.setMinimumWidth(180)
        btn.setFixedHeight(26)
        btn.setStyleSheet(styles.TOOL_BUTTON_STYLE)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda: (self._play_click(), self.tool_changed.emit(tool_type)))
        return btn
    
    def create_color_button(self, color: QColor) -> QPushButton:
        """Создать кнопку выбора цвета"""
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setFixedSize(40, 40)
        btn.setCursor(Qt.PointingHandCursor)
        
        # Создаем стиль с заливкой цветом
        style = f'''
            QPushButton {{
                background-color: {color.name()};
                border: 2px solid transparent;
                border-radius: 20px;
            }}
            QPushButton:hover {{
                border: 2px solid rgba(255, 255, 255, 0.3);
            }}
            QPushButton:checked {{
                border: 3px solid #FFD93D;
            }}
        '''
        btn.setStyleSheet(style)
        btn.clicked.connect(lambda: (self._play_click(), self.color_changed.emit(color)))
        return btn
    
    def _load_button_icon(self, button: QPushButton, icon_file: str, tooltip: str) -> None:
        """Загрузить SVG иконку для кнопки"""
        from PyQt5.QtSvg import QSvgRenderer
        from PyQt5.QtGui import QPixmap, QPainter, QIcon
        import os
        
        button.setToolTip(tooltip)
        
        icon_path = os.path.join('assets', 'icons', icon_file)
        if os.path.exists(icon_path):
            pixmap = QPixmap(20, 20)
            pixmap.fill(Qt.transparent)
            
            renderer = QSvgRenderer(icon_path)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            
            button.setIcon(QIcon(pixmap))
            button.setIconSize(pixmap.size())
    
    def create_separator(self) -> QLabel:
        """Создать разделительную линию"""
        separator = QLabel()
        separator.setFixedHeight(1)
        separator.setStyleSheet('background-color: #666;')
        return separator
    
    def on_width_changed(self, value: int) -> None:
        """Обработка изменения толщины линии"""
        self.width_value_label.setText(f'{value} px')
        self.width_changed.emit(value)
    
    def on_toggle_drawing(self) -> None:
        """Обработка переключения режима рисования"""
        self.drawing_mode = self.toggle_btn.isChecked()
        if self.drawing_mode:
            self.toggle_btn.setText('ВЫКЛЮЧИТЬ\nРИСОВАНИЕ')
            print('🟢 Кнопка: Режим рисования ВКЛЮЧЕН')
        else:
            self.toggle_btn.setText('ВКЛЮЧИТЬ\nРИСОВАНИЕ')
            print('🔴 Кнопка: Режим рисования ВЫКЛЮЧЕН')
        
        self._play_click()
        self.toggle_drawing_requested.emit()
    
    def update_drawing_mode(self, enabled: bool) -> None:
        """Обновить состояние кнопки переключения (вызывается извне)"""
        self.drawing_mode = enabled
        self.toggle_btn.setChecked(enabled)
        if enabled:
            self.toggle_btn.setText('ВЫКЛЮЧИТЬ\nРИСОВАНИЕ')
        else:
            self.toggle_btn.setText('ВКЛЮЧИТЬ\nРИСОВАНИЕ')
    
    def _play_click(self):
        """Воспроизвести звук клика"""
        if self.sound_manager:
            self.sound_manager.play_click()
    
    # Методы для перетаскивания панели
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Начало перетаскивания"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Перетаскивание панели"""
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            self.geometry_changed.emit()  # Уведомляем об изменении позиции
            event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Конец перетаскивания"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
